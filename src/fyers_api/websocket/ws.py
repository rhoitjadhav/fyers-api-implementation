import os
import json
import time
import asyncio
import logging
import traceback
import urllib
import requests
from struct import Struct
from websockets import connect
from logging.config import dictConfig

CURRENT_FOLDER = os.path.dirname(os.path.abspath(__file__))


class FyersSocket():

	def __init__(self, access_token=None, data_type=None, symbol=None):
		self.access_token = access_token # access token of the user
		self.data_type = data_type # type of data requested by the user
		self.ws_link = None
		self.ws = None 
		self.connected_flag = True
		self.transmit_flag = True
		self.receive_flag = False
		self.transmit_message = None
		self.data = None
		self.reconnect_counter = 0
		self.reconnect_flag = False
		self.symbol = symbol
		self.message = None
		self.response_out = {"s":"","code":"","message":""}
		self.data_url = "https://api.fyers.in/data-rest/v2/quotes/"
		self.content = 'application/json'
		self.get_symtoken = []
		self.update_symbol = ""
		
		# logger setup
		self.logger_setup()
		self.logger.info("Initiate socket object")
		self.logger.debug('access_token ' + self.access_token)
		# log file path
		self.log_path = os.path.join(CURRENT_FOLDER, 'fyers_socket.log')

		# struct init
		self.FY_P_ENDIAN	    = '> '
		self.FY_P_HEADER_FORMAT = Struct(self.FY_P_ENDIAN + "Q L H H H 6x")
		self.FY_P_COMMON_7208   = Struct(self.FY_P_ENDIAN + "10I Q")
		self.FY_P_EXTRA_7208    = Struct(self.FY_P_ENDIAN + "4I 2Q")
		self.FY_P_MARKET_PIC    = Struct(self.FY_P_ENDIAN + "3I")
		self.FY_P_LENGTH        = Struct(self.FY_P_ENDIAN + "H")

		# packet length define
		self.FY_P_LEN_NUM_PACKET 	= 2
		self.FY_P_LEN_HEADER 		= 24
		self.FY_P_LEN_COMN_PAYLOAD	= 48 
		self.FY_P_LEN_EXTRA_7208	= 32 
		self.FY_P_LEN_BID_ASK 		= 12 
		self.FY_P_BID_ASK_CNT 		= 10
		self.FY_P_LEN_RES           = 6 

		# Aux
		self.counter = 0

		# Results
		self.response = None

	def logger_setup(self):
		LOGGING = {
			'version': 1,
			'disable_existing_loggers': False,
			'formatters': {
				'verbose': {
					'format': '%(asctime)s - %(name)s - %(levelname)s - %(pathname)s - %(lineno)d - %(message)s'
				}
			},
			'handlers': {
				'console': {
					'class': 'logging.StreamHandler',
					'level': 'DEBUG',
					'formatter': 'verbose',
				},
				'file': {
					'class': 'logging.FileHandler',
					'level': 'DEBUG',
					'formatter': 'verbose',
					'filename': os.path.join(CURRENT_FOLDER, 'fyers_socket.log')
				}
			},
			'loggers': {
				'fyers_socket': {
					'handlers': ['file'],
					'level': 'DEBUG',
					'propagate': False,
				}
			},
		}

		dictConfig(LOGGING)
		self.logger = logging.getLogger('fyers_socket')

	def on_message(self):
		"""
			Called when a new message is received from websocket
		"""
		if self.data == '"pong"':
			# print("pong received")
			pass
		if self.data_type == "symbolData":
			self.response = self.parse_symbol_data()
		else:
			self.response = self.data

		# print(self.data)
		return


	def websocket_data(self):
		return


	def verify_msg(self,msg):
		try:
			if type(msg) == str:
				msg = json.loads(msg)
			self.response_out["s"] = msg["s"]
			if "code" in msg:
				self.response_out["code"] = msg["code"]
				self.response_out["message"] = msg["message"] 
			# print(f"response:{self.response_out}")
			return self.response_out
		except Exception as e:
			self.logger.error(str(traceback.format_exc()))

	def export_data(self, packet_data):
		self.counter += 1
		location = "/home/fyers/fyers/fyers-api-py/websocket/data/biocon"
		if not os.path.exists(location):
			os.makedirs(location)

		with open(os.path.join(location, str(self.counter) + ".json"), 'w+') as outfile:
			json.dump(packet_data, outfile)


	def parse_symbol_data(self):
		"""
			Called when data_type is symbolData
		"""
		self.message = self.data
		packet_length = int(len(self.message)/224)
		if packet_length == 0:
			return []
		# (packet_length, ) = self.FY_P_LENGTH.unpack(self.message[:self.FY_P_LEN_NUM_PACKET])
		decrypted_packet_items = []

		for i in range(packet_length):
			(fyToken, timestamp, fyCode, fyFlag, pktLen) = self.FY_P_HEADER_FORMAT.unpack(self.message[:self.FY_P_LEN_HEADER])
			# print(f"string_msg:{self.FY_P_HEADER_FORMAT.unpack(self.message[:self.FY_P_LEN_HEADER])}")
			for fytoken_sym in self.get_symtoken:
				if fyToken == int(fytoken_sym["fy_token"]):
					self.update_symbol = fytoken_sym["symbol"]
					# print(f"symbol:{self.update_symbol}")
			packet_data = {"symbol": self.update_symbol, "timestamp": timestamp, "fyCode": fyCode, "fyFlag": fyFlag, "pktLen": pktLen}
			self.message = self.message[self.FY_P_LEN_HEADER:]

			pc, ltp, op, hp, lp, cp, mop, mhp, mlp, mcp, mv = self.FY_P_COMMON_7208.unpack(self.message[: self.FY_P_LEN_COMN_PAYLOAD])
			
			packet_data["ltp"] = ltp/pc
			packet_data["open_price"] = op/pc
			packet_data["high_price"] = hp/pc
			packet_data["low_price"] = lp/pc
			packet_data["close_price"] = cp/pc
			packet_data["min_open_price"] = mop/pc
			packet_data["min_high_price"] = mhp/pc
			packet_data["min_low_price"] = mlp/pc
			packet_data["min_close_price"] = mcp/pc
			packet_data["min_volume"] = mv
			
			self.message = self.message[self.FY_P_LEN_COMN_PAYLOAD:]
			ltq, ltt, atP, vtt, totBuy, totSell = self.FY_P_EXTRA_7208.unpack(self.message[: self.FY_P_LEN_EXTRA_7208])
			packet_data["last_traded_qty"] = ltq
			packet_data["last_traded_time"] = ltt
			packet_data["avg_trade_price"] = atP
			packet_data["vol_traded_today"] = vtt
			packet_data["tot_buy_qty"] = totBuy
			packet_data["tot_sell_qty"] = totSell
			
			packet_data["market_pic"] = []
			
			self.message = self.message[self.FY_P_LEN_EXTRA_7208:]
			for i in range(0, 10):
				prc, qty, num_ord = self.FY_P_MARKET_PIC.unpack(self.message[:self.FY_P_LEN_BID_ASK])
				packet_data["market_pic"].append({"price": prc/pc, "qty": qty, "num_orders": num_ord})
				self.message = self.message[self.FY_P_LEN_BID_ASK:]
				
			self.data = packet_data
			# print(f"packet_data:{packet_data}")
			decrypted_packet_items.append(packet_data)
			# self.export_data(packet_data)
		return decrypted_packet_items


	def on_error(self):
		print("error please view the fyers_socket.logs")
		return 


	def on_close(self):
		print("### closed ###")


	def close_socket(self):
		self.connected_flag = False


	def reset_reconnect_counter(self):
		self.reconnect_flag = False
		self.reconnect_counter = 0


	def reconnect(self):
		"""
			will check the counter and initiate reconnection
		"""
		
		if self.reconnect_counter < 3:
			self.logger.info("reconnecting initiating in 10 seconds")
			time.sleep(10)
			self.connected_flag = True
			self.reconnect_counter += 1
			self.receive()
		else:
			self.connected_flag = False
			self.logger.critical("reconnecting failed, please check your network")  

	async def ping1(self,websocket):
		while True:
			await websocket.send(json.dumps("ping"))
			await asyncio.sleep(5)

	def socket_data_define(self,symbol= "",unsubscribe_flag=False):
		"""
			Map requested data_type to trasmit message for subscription
		"""
		self.transmit_flag = True
		self.logger.info("requesting data for " + self.data_type)

		if symbol != "":
			self.symbol = symbol

		if unsubscribe_flag == True:
			SUB_T = 0
		else:
			SUB_T = 1
		
		if self.data_type == "orderUpdate":
			self.transmit_message = {"T":"SUB_ORD", "SLIST":["orderUpdate"], "SUB_T": SUB_T}
			self.ws_link = "wss://api.fyers.in/socket/v2/orderSock?type=orderUpdate&access_token="+ self.access_token +"&user-agent=fyers-api"
	
		elif self.data_type == "symbolData":
			self.transmit_message = {"T":"SUB_L2","L2LIST":self.symbol,"SUB_T":SUB_T}
			self.ws_link = "wss://api.fyers.in/socket/v2/dataSock?access_token=" + self.access_token
			symbols = self.symbol
			symbols_dict= {"symbols":""}
			symbols_dict["symbols"]= ','.join(symbols)
			url_params = urllib.parse.urlencode(symbols_dict)
			url =  self.data_url+ "?" + url_params
			get_quotes = requests.get(url=url, headers={"Authorization": self.access_token, 'Content-Type': self.content})
			quotes_response = get_quotes.json()
			if quotes_response["s"]== "error":
				self.response_out["s"]= quotes_response["s"]
				self.response_out["code"]=quotes_response["code"]
				self.response_out["message"]=quotes_response["message"]
				return self.response_out
			for symbol in quotes_response["d"]:
				symbol_data=symbol["v"]["symbol"]
				fy_token = symbol["v"]["fyToken"]
				data_dict = {"fy_token":fy_token,"symbol":symbol_data}
				self.get_symtoken.append(data_dict)
	
		else:
			self.response_out["s"]="error"
			self.response_out["code"]=324
			self.response_out["message"]="please provide valid dataType"
			return self.response_out
		# self.ws = connect("wss://data.fyers.in/dataSockDev?token_id=<tokenHash>&type=orderUpdate")
		
		self.ws = connect(self.ws_link)
		# print("link", self.ws_link)
		self.logger.info("Connection Initiated")

	async def start_stream(self):
		async with self.ws as websocket:
			if self.connected_flag:
				asyncio.ensure_future(self.ping1(websocket))

			while self.connected_flag:
				
				if self.receive_flag:
					
					if websocket.open:
						self.reset_reconnect_counter()
						try:
							msg = await websocket.recv()
							# print("msg:", msg)
							if type(msg)==str:
								if "error" in msg:
									msg = json.loads(msg)
									processed_response = self.verify_msg(msg=msg)
									self.connected_flag= False
									self.reconnect_flag = False
									# self.response = {"s":"error","code":msg["code"],"message":msg["message"]}
									# print(f"processed_response:{processed_response}")
									
								else:
									self.data = msg
									self.on_message()
									self.websocket_data()
							else:
								self.data = msg
								self.on_message()
								self.websocket_data()
						except Exception as e:
							self.logger.error(str(traceback.format_exc()))
							self.logger.debug(self.message)
							print("Exception is", e)

					else:
						self.reconnect_flag = True
						self.connected_flag = False

				if self.transmit_flag:
					t = await websocket.send(json.dumps(self.transmit_message))
					# print("Trmsg:", self.transmit_message)
					self.logger.info("transmitted connection settings")
					self.transmit_flag = False
					self.receive_flag = True
		

	def subscribe(self):
		resp = self.socket_data_define()
		if str(resp)!= "None":
			if resp["s"] == "error":
				self.logger.error(resp)
				# return print(resp)
				return
		try:
			asyncio.get_event_loop().run_until_complete(self.start_stream()) 
		except Exception as e:
			# print("Sdsdfsdf:", e)
			self.logger.error(e)
			self.logger.error(str(traceback.format_exc()))

			self.logger.info("Initiating reconnection after failure")
			if self.reconnect_flag:
				self.reconnect()

	def unsubscribe(self,symbol):
		resp = self.socket_data_define(symbol,unsubscribe_flag=True)
		if str(resp)!= "None":
			if resp["s"] == "error":
				self.logger.error(resp)
				# return print(resp)
				return
		try:
			asyncio.get_event_loop().run_until_complete(self.start_stream()) 
		except Exception as e:
			self.logger.error(e)
			self.logger.error(str(traceback.format_exc()))

			self.logger.info("Initiating reconnection after failure")
			if self.reconnect_flag:
				self.reconnect()

   

	
if __name__ == "__main__":
    	
	pass
	# # API V2
	# access_token = "TWQFQCS0Q4-101:eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJhcGkuZnllcnMuaW4iLCJpYXQiOjE2MjM5MTMyMDEsImV4cCI6MTYyMzk3NjIwMSwibmJmIjoxNjIzOTEzMjAxLCJhdWQiOlsieDoyIiwieDoxIiwieDowIiwiZDoxIiwiZDoyIl0sInN1YiI6ImFjY2Vzc190b2tlbiIsImF0X2hhc2giOiJnQUFBQUFCZ3l2THhSWHVLSGxYWGU2YmNNR0RQcU84TDJqNmxVUlJJd0RGU2NzcDMyU2JSZzlYQVhzTW5JRVRNT3l1TEJXc2NkZEduY0FVUmVaTWZNYTdaTmhzT0FlS3NHS1dSQV9WTUNYaVdvOXBuMVFsZEpyST0iLCJkaXNwbGF5X25hbWUiOiJQSVlVU0ggUkFKRU5EUkEgS0FQU0UiLCJmeV9pZCI6IkRQMDA0MDQiLCJhcHBUeXBlIjoxMDEsInBvYV9mbGFnIjoiTiJ9.s7lmDQ6ITzXKkkevY40qcgZ7gm5SJGxWUyLzQQX9tHk"
	
	# # # # API V1
	# # # # access_token ="zqyEYv3aLvkZX58xHtJFJbBr4j-kyHYoPdICS5x7EWaV7FinVtLpmLI6FL26umhhRXekXANXZow="
	
	# data_type = "orderUpdate"
	# data_type = "symbolData"

	# # # symbol = "NSE:PNB-EQ"
	# # # # symbol = "NSE:SBIN-EQ"
	# # # symbol = "NSE:BIOCON-EQ"
	# # # # symbol = "BSE:PNB-A" 
	# symbol = ["NSE:SBIN-EQ","NSE:ONGC-EQ","NSE:PNB-EQ","NSE:IOC-EQ","MCX:SILVERMIC21JUNFUT","MCX:ALUMINIUM21JUNFUT"]
	# # # # symbol = ""
	# def custom_message(self):
	# 	print ("Custom " + str(self.response))    
	
	# FyersSocket.websocket_data = custom_message 
	# fs = FyersSocket(access_token=access_token, data_type=data_type,symbol=symbol)
	# # # fs.set_log_path('/home/fyers/socksock.log')
	# # symbol = ["MCX:ALUMINIUM21JUNFUT"]
	# # print("entered unsubcribe function")
	# # fs.unsubscribe(symbol=symbol)
	# fs.subscribe()

 