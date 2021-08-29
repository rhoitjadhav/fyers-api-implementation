moduleName ="fyersModel"
try:
	from .fyersService import FyersService
	from .fyersService import FyersAsyncService
	import json
	from .config import Config
	import subprocess
	import sys
	from datetime import datetime, timezone
	from .fyersLog import FyersLog

except Exception as e:
	print("moduleName: {}, ERR: could not import module : {}".format(moduleName,e))


class FyersModel:
	def __init__(self, is_async=False, client_id=None, token="", log_path = ""):
		self.client_id = client_id
		self.token = token
		self.log_path = log_path
		self.logObj = FyersLog(self.log_path)
		self.header = "{}:{}".format(self.client_id, self.token)
		if is_async:
			self.service = FyersAsyncService(self.logObj)
		else:
			self.service = FyersService(self.logObj)

	def create_timestamp(self):
		try:
			return str(int(datetime.now(tz=timezone.utc).timestamp() * 1000))
		except Exception as e:
			self.logObj.logEntryFunc(str(int(datetime.now(tz=timezone.utc).timestamp() * 1000)), "create_timestamp", "", "", "ERROR  : {}".format(e))
			return

	def get_profile(self):
		try:
			timestamp = self.create_timestamp()
			# response = self.service.getCall(Config.get_profile, self.token)
			response = self.service.getCall(Config.get_profile,self.header)
			self.logObj.logEntryFunc(timestamp, "get_profile", self.header, response)
			return response
		except Exception as e:
			self.logObj.logEntryFunc(str(int(datetime.now(tz=timezone.utc).timestamp() * 1000)), "get_profile", "", "response", "ERROR  : {}".format(e))
			return

	def tradebook(self, data=None):
		try:
			timestamp = self.create_timestamp()
			response = self.service.getCall(Config.tradebook, self.header, data=data)
			self.logObj.logEntryFunc(timestamp,"tradebook", data, response)
			return response
		except Exception as e:
			self.logObj.logEntryFunc(str(int(datetime.now(tz=timezone.utc).timestamp() * 1000)), "tradebook", "", "", "ERROR  : {}".format(e))
			return

	def positions(self):
		try:
			timestamp = self.create_timestamp()
			response = self.service.getCall(Config.positions, self.header)
			self.logObj.logEntryFunc(timestamp, "positions", "", response)
			return response
		except Exception as e:
			self.logObj.logEntryFunc(str(int(datetime.now(tz=timezone.utc).timestamp() * 1000)), "positions", "", "response", "ERROR  : {}".format(e))
			return

	def holdings(self,data=None):
		try:
			timestamp = self.create_timestamp()
			response = self.service.getCall(Config.holdings, self.header, data=data)
			self.logObj.logEntryFunc(timestamp, "holdings", data, response)
			return response
		except Exception as e:
			self.logObj.logEntryFunc(str(int(datetime.now(tz=timezone.utc).timestamp() * 1000)), "holdings", data, "response", "ERROR  : {}".format(e))
			return

	def convert_position(self,data):
		try:
			timestamp = self.create_timestamp()
			response = self.service.putCall(Config.convertPosition, self.header, data)
			self.logObj.logEntryFunc(timestamp, "convert_position", data, response)
			return response
		except Exception as e:
			self.logObj.logEntryFunc(str(int(datetime.now(tz=timezone.utc).timestamp() * 1000)), "convert_position", "", "response", "ERROR  : {}".format(e))
			return

	def funds(self,data=None):
		try:
			timestamp = self.create_timestamp()
			response = self.service.getCall(Config.funds, self.header, data=data)
			self.logObj.logEntryFunc(timestamp, "funds", data, response)
			return response
		except Exception as e:
			self.logObj.logEntryFunc(str(int(datetime.now(tz=timezone.utc).timestamp() * 1000)), "funds", data, "response", "ERROR  : {}".format(e))
			return

	def orderbook(self, data=None):
		try:
			timestamp = self.create_timestamp()
			response = self.service.getCall(Config.orders, self.header, data=data)
			self.logObj.logEntryFunc(timestamp, "orderBook", "", response)
			return response
		except Exception as e:
			self.logObj.logEntryFunc(str(int(datetime.now(tz=timezone.utc).timestamp() * 1000)), "orderBook", "", "response", "ERROR  : {}".format(e))
			return

	def cancel_order(self,data):
		try:
			timestamp = self.create_timestamp()
			response = self.service.deleteCall(Config.orders, self.header, data)
			self.logObj.logEntryFunc(timestamp, "cancel_order", data, response)
			return response
		except Exception as e:
			self.logObj.logEntryFunc(str(int(datetime.now(tz=timezone.utc).timestamp() * 1000)), "cancel_orders", data, "response", "ERROR  : {}".format(e))
			return

	def place_order(self,data):
		try:
			timestamp = self.create_timestamp()
			response = self.service.postCall(Config.orders, self.header, data)
			self.logObj.logEntryFunc(timestamp, "place_order", "", response)
			return response
		except Exception as e:
			self.logObj.logEntryFunc(str(int(datetime.now(tz=timezone.utc).timestamp() * 1000)), "place_orders", data, "response", "ERROR  : {}".format(e))
			return

	def modify_order(self,data):
		try:
			timestamp = self.create_timestamp()
			response = self.service.putCall(Config.orders, self.header, data)
			self.logObj.logEntryFunc(timestamp, "modify_order", data, response)
			return response
		except Exception as e:
			self.logObj.logEntryFunc(str(int(datetime.now(tz=timezone.utc).timestamp() * 1000)), "modify_orders", data, "response", "ERROR  : {}".format(e))
			return

	def minquantity(self):
		try:
			timestamp = self.create_timestamp()
			response = self.service.getCall(Config.minquantity, self.header)
			self.logObj.logEntryFunc(timestamp, "minquantity", self.header, response)
			return response
		except Exception as e:
			self.logObj.logEntryFunc(str(int(datetime.now(tz=timezone.utc).timestamp() * 1000)), "minquantity", self.header, "response", "ERROR  : {}".format(e))
			return

	def market_status(self):
		try:
			timestamp = self.create_timestamp()
			response = self.service.getCall(Config.marketStatus, self.header)
			self.logObj.logEntryFunc(timestamp, "market_status", "", response)
			return response
		except Exception as e:
			self.logObj.logEntryFunc(str(int(datetime.now(tz=timezone.utc).timestamp() * 1000)), "market_status", "", "response", "ERROR  : {}".format(e))
			return

	def exit_positions(self,data=None):
		try:
			timestamp = self.create_timestamp()
			response = self.service.deleteCall(Config.exitPositions, self.header, data)
			self.logObj.logEntryFunc(timestamp, "exit_positions", data, response)
			return response
		except Exception as e:
			self.logObj.logEntryFunc(str(int(datetime.now(tz=timezone.utc).timestamp() * 1000)), "exit_positions", data, "response", "ERROR  : {}".format(e))
			return

	def generate_data_token(self,data):
		try:
			timestamp = self.create_timestamp()
			allPackages = subprocess.check_output([sys.executable, '-m', 'pip', 'freeze'])
			installed_packages = [r.decode().split('==')[0] for r in allPackages.split()]
			if Config.dataVendorTD not in installed_packages:
				print("Please install truedata package | pip install truedata-ws")
			response = self.service.postCall(Config.generateDataToken, self.header, data)
			self.logObj.logEntryFunc(timestamp, "generate_data_token", data, response)
			return response
		except Exception as e:
			self.logObj.logEntryFunc(str(int(datetime.now(tz=timezone.utc).timestamp() * 1000)), "generate_data_token", "", "response", "ERROR  : {}".format(e))
			return

	def get_orders(self,data):
		try:
			timestamp = self.create_timestamp()
			response = self.service.getCall(Config.multi_orders, self.header, data=data)
			self.logObj.logEntryFunc(timestamp, "multiple_orders", data, response)
			return response
		except Exception as e:
			self.logObj.logEntryFunc(str(int(datetime.now(tz=timezone.utc).timestamp() * 1000)), "multiple_orders", data, "response", "ERROR  : {}".format(e))
			return

	def cancel_basket_orders(self,data):
		try:
			timestamp = self.create_timestamp()
			response = self.service.deleteCall(Config.multi_orders, self.header, data)
			self.logObj.logEntryFunc(timestamp,"cancel_basket_orders", data, response)
			return response
		except Exception as e:
			self.logObj.logEntryFunc(str(int(datetime.now(tz=timezone.utc).timestamp() * 1000)), "cancel_basket_orders", data, "response", "ERROR  : {}".format(e))
			return

	def place_basket_orders(self,data):
		try:
			timestamp = self.create_timestamp()
			response = self.service.postCall(Config.multi_orders, self.header, data)
			self.logObj.logEntryFunc(timestamp, "place_basket_orders", data, response)
			return response
		except Exception as e:
			self.logObj.logEntryFunc(str(int(datetime.now(tz=timezone.utc).timestamp() * 1000)), "place_basket_orders", data, "response", "ERROR  : {}".format(e))
			return

	def modify_basket_orders(self,data):
		try:
			timestamp = self.create_timestamp()
			response = self.service.putCall(Config.multi_orders, self.header, data)
			self.logObj.logEntryFunc(timestamp, "modify_basket_orders", data, response)
			return response
		except Exception as e:
			self.logObj.logEntryFunc(str(int(datetime.now(tz=timezone.utc).timestamp() * 1000)), "modify_basket_orders", data, "response", "ERROR  : {}".format(e))
			return

	def history(self,data=None):
		try: 
			timestamp = self.create_timestamp()
			response = self.service.getCall(Config.history, self.header, data,data_flag=True)
			self.logObj.logEntryFunc(timestamp, "history", data, response)
			return response
		except Exception as e:
			self.logObj.logEntryFunc(str(int(datetime.now(tz=timezone.utc).timestamp() * 1000)), "history", data, "response", "ERROR  : {}".format(e))
			return

	def quotes(self,data=None):
		try: 
			timestamp = self.create_timestamp()
			response = self.service.getCall(Config.quotes, self.header, data,data_flag=True)
			self.logObj.logEntryFunc(timestamp, "quotes", data, response)
			return response
		except Exception as e:
			self.logObj.logEntryFunc(str(int(datetime.now(tz=timezone.utc).timestamp() * 1000)), "history", data, "response", "ERROR  : {}".format(e))
			return

	def depth(self,data=None):
		try: 
			timestamp = self.create_timestamp()
			response = self.service.getCall(Config.market_depth, self.header, data,data_flag=True)
			self.logObj.logEntryFunc(timestamp, "depth", data, response)
			return response
		except Exception as e:
			self.logObj.logEntryFunc(str(int(datetime.now(tz=timezone.utc).timestamp() * 1000)), "history", data, "response", "ERROR  : {}".format(e))
			return