from threading import Thread
from requests.models import Response
from fyers_api.Websocket import constants
from typing import Any, Dict
import json
import urllib
import requests
import websocket
import logging
from logging.config import dictConfig
import os
from time import sleep
from fyers_api.fyersLog import FyersLog
import sys


class FyersSocket:
    def __init__(self, access_token=None, run_background=False, log_path=None):
        self.__access_token = access_token
        self.__data_type = None
        self.__symbols = []
        self.__websocket = None
        self.__ws_url = None
        self.__ws_object = None
        self.__ws_run = False
        self.__ws_message = None
        self.log_path = log_path
        self.data_url = "https://api.fyers.in/data-rest/v2/quotes/"
        self.content = 'application/json'
        self.run_background = run_background
        self.background_flag = False
        self.get_symtoken = []
        self.response_out = {"s": "", "code": "", "message": ""}
        self.response = None
        self.t = None
        self.websocket_data = None
        self.on_open = None
        self.on_error = None
        ##logger setup
        self.logger_setup()
        self.logger.info("Initiate socket object")
        self.logger.debug('access_token ' + self.__access_token)
        # log file path
        self.log_path = os.path.join(self.log_path, 'fyers_socket.log')

    def __get_ws_link(self):
        if self.__data_type == constants.KEY_ORDER_UPDATE:
            return constants.WS_ORDERS_URL.format(access_token=self.__access_token)
        elif self.__data_type == constants.KEY_DATA_UPDATE:
            return constants.WS_DATA_URL.format(access_token=self.__access_token)

    def init_connection(self):
        if self.run_background:
            self.background_flag = True
        self.__ws_url = self.__get_ws_link()
        ws = websocket.WebSocketApp(
            self.__ws_url,
            on_message=lambda ws, msg: self.__on_message(ws, msg),
            on_error=lambda ws, msg: self.__on_error(ws, msg),
            on_close=lambda ws, a, b: self.__on_close(ws, a, b),
            on_open=lambda ws: self.__on_open(ws),
        )
        self.t = Thread(target=ws.run_forever)
        self.t.daemon = self.background_flag
        self.t.start()

    def keep_running(self):
        self.__ws_run = True
        t = Thread(target=self.infinite_loop)
        t.start()

    # t.join()

    def stop_running(self):
        self.__ws_run = False

    def set_message_override(self, f):
        self.__ws_message = f

    def infinite_loop(self):
        while (self.__ws_run):
            pass

    def subscribe(self, symbol=None, data_type=None):
        self.__data_type = data_type
        self.init_connection()
        sleep(2)
        if symbol != None:
            if len(symbol) > 0:
                if symbol not in self.__symbols:
                    self.__symbols.extend(symbol)
        else:
            symbol = ""
        if self.__ws_object is not None:
            get_symbol_data = self.__construct_send_message(symbol=symbol)
            if isinstance(get_symbol_data, dict):
                if get_symbol_data["s"] == "error":
                    self.response_out["s"] = get_symbol_data["s"]
                    self.response_out["code"] = get_symbol_data["code"]
                    self.response_out["message"] = get_symbol_data["message"]
                    self.response = self.response_out
                    print(self.response)
            else:
                self.__ws_object.send(get_symbol_data)
                if self.run_background is False:
                    self.t.join()

    def unsubscribe(self, symbol):
        # self.init_connection()
        self.logger.debug("entered unsubscribe method")
        self.__symbols = [item for item in self.__symbols if item not in symbol]
        if self.__ws_object is not None:
            self.__ws_object.send(self.__construct_send_message(symbol=symbol, unsubscribe_flag=True))

    def __construct_send_message(self, symbol="", unsubscribe_flag=False):
        if unsubscribe_flag == True:
            SUB_T = 0
        else:
            SUB_T = 1
        if self.__data_type == constants.KEY_ORDER_UPDATE:
            message = {"T": "SUB_ORD", "SLIST": [], "SUB_T": SUB_T}
            message["SLIST"] = constants.KEY_ORDER_UPDATE
        elif self.__data_type == constants.KEY_DATA_UPDATE:
            message = {"T": "SUB_L2", "L2LIST": [], "SUB_T": SUB_T}
            message["L2LIST"] = symbol
            symbols = symbol
            symbols_dict = {"symbols": ""}
            symbols_dict["symbols"] = ','.join(symbols)
            url_params = urllib.parse.urlencode(symbols_dict)
            url = self.data_url + "?" + url_params
            url = urllib.parse.unquote(url, encoding="utf-8")
            get_quotes = requests.get(url=url,
                                      headers={"Authorization": self.__access_token, 'Content-Type': self.content})
            quotes_response = get_quotes.json()
            if quotes_response["s"] == "error":
                self.response_out["s"] = quotes_response["s"]
                self.response_out["code"] = quotes_response["code"]
                self.response_out["message"] = quotes_response["message"]
                return self.response_out
            for symbol in quotes_response["d"]:
                symbol_data = symbol["v"]["symbol"]
                fy_token = symbol["v"]["fyToken"]
                data_dict = {"fy_token": fy_token, "symbol": symbol_data}
                self.get_symtoken.append(data_dict)
        # message["SUB_T"] = int(subscribe)
        return json.dumps(message)

    def __on_message(self, ws, msg):
        if self.__data_type == "symbolData":
            self.response = self.parse_symbol_data(msg)
            if self.background_flag:
                if type(msg) == str:
                    if "error" in msg:
                        msg = json.loads(msg)
                        self.response_out["s"] = msg["s"]
                        self.response_out["code"] = msg["code"]
                        self.response_out["message"] = msg["message"]
                        self.response = self.response_out
                        self.logger.error("Response:{self.response}")
                self.logger.debug(f"Response:{self.response}")
            else:
                if type(msg) == str:
                    if "error" in msg:
                        msg = json.loads(msg)
                        self.response_out["s"] = msg["s"]
                        self.response_out["code"] = msg["code"]
                        self.response_out["message"] = msg["message"]
                        self.response = self.response_out
                        self.logger.error(self.response)
                        if self.websocket_data is not None:
                            self.websocket_data(self.response)
                        else:
                            print(f"Response:{self.response}")
                else:
                    if self.websocket_data is not None:
                        self.websocket_data(self.response)
                    else:
                        print(f"Response:{self.response}")
            # self.logger.debug(self.response)
        else:
            self.response = msg
            if self.background_flag:
                if type(msg) == str:
                    if "error" in msg:
                        msg = json.loads(msg)
                        self.response_out["s"] = msg["s"]
                        self.response_out["code"] = msg["code"]
                        self.response_out["message"] = msg["message"]
                        self.response = self.response_out
                        self.logger.error(self.response)
                self.logger.debug(f"Response:{self.response}")
            else:
                if type(msg) == str:
                    if "error" in msg:
                        msg = json.loads(msg)
                        self.response_out["s"] = msg["s"]
                        self.response_out["code"] = msg["code"]
                        self.response_out["message"] = msg["message"]
                        self.response = self.response_out
                        self.logger.error(self.response)
                        if self.websocket_data is not None:
                            self.websocket_data(self.response)
                        else:
                            print(f"Response:{self.response}")
                    else:
                        if self.websocket_data is not None:
                            self.websocket_data(self.response)
                        else:
                            print(f"Response:{self.response}")
                else:
                    if self.websocket_data is not None:
                        self.websocket_data(self.response)
                    else:
                        print(f"Response:{self.response}")
        # self.websocket_data()
        return

    # if self.__ws_message is not None:
    #     self.__ws_message(msg)

    def parse_symbol_data(self, msg):
        """
            Called when data_type is symbolData
        """
        try:
            self.message = msg
            if isinstance(self.message, str):
                return []

            # import ipdb;ipdb.set_trace()
            # packet_length = int(len(self.message)/224)
            # if packet_length == 0:
            # 	return []
            # (packet_length, ) = self.FY_P_LENGTH.unpack(self.message[:self.FY_P_LEN_NUM_PACKET])
            decrypted_packet_items = []

            for i in range(len(msg)):
                if len(self.message) == 0:
                    continue
                (fyToken, timestamp, fyCode, fyFlag, pktLen) = constants.FY_P_HEADER_FORMAT.unpack(
                    self.message[:constants.FY_P_LEN_HEADER])
                # print(f"string_msg:{self.FY_P_HEADER_FORMAT.unpack(self.message[:self.FY_P_LEN_HEADER])}")
                if str(fyToken)[:2] not in ["10", "11", "12"]:
                    continue
                for fytoken_sym in self.get_symtoken:
                    if fyToken == int(fytoken_sym["fy_token"]):
                        self.update_symbol = fytoken_sym["symbol"]
                packet_data = {"symbol": self.update_symbol, "timestamp": timestamp, "fyCode": fyCode, "fyFlag": fyFlag,
                               "pktLen": pktLen}
                self.message = self.message[constants.FY_P_LEN_HEADER:]

                pc, ltp, op, hp, lp, cp, mop, mhp, mlp, mcp, mv = constants.FY_P_COMMON_7208.unpack(
                    self.message[: constants.FY_P_LEN_COMN_PAYLOAD])

                packet_data["ltp"] = ltp / pc
                packet_data["open_price"] = op / pc
                packet_data["high_price"] = hp / pc
                packet_data["low_price"] = lp / pc
                packet_data["close_price"] = cp / pc
                packet_data["min_open_price"] = mop / pc
                packet_data["min_high_price"] = mhp / pc
                packet_data["min_low_price"] = mlp / pc
                packet_data["min_close_price"] = mcp / pc
                packet_data["min_volume"] = mv
                # print(fyToken, timestamp, fyCode, fyFlag, pktLen)
                # print(fyCode,type(fyCode))
                if int(fyCode) not in [7202, 7207, 27]:
                    self.message = self.message[constants.FY_P_LEN_COMN_PAYLOAD:]
                    ltq, ltt, atP, vtt, totBuy, totSell = constants.FY_P_EXTRA_7208.unpack(
                        self.message[: constants.FY_P_LEN_EXTRA_7208])
                    packet_data["last_traded_qty"] = ltq
                    packet_data["last_traded_time"] = ltt
                    packet_data["avg_trade_price"] = atP
                    packet_data["vol_traded_today"] = vtt
                    packet_data["tot_buy_qty"] = totBuy
                    packet_data["tot_sell_qty"] = totSell

                    packet_data["market_pic"] = []

                    self.message = self.message[constants.FY_P_LEN_EXTRA_7208:]
                    for i in range(0, 10):
                        prc, qty, num_ord = constants.FY_P_MARKET_PIC.unpack(self.message[:constants.FY_P_LEN_BID_ASK])
                        packet_data["market_pic"].append({"price": prc / pc, "qty": qty, "num_orders": num_ord})
                        self.message = self.message[constants.FY_P_LEN_BID_ASK:]

                self.data = packet_data
                decrypted_packet_items.append(packet_data)
                self.response = decrypted_packet_items
            return decrypted_packet_items
        except Exception as e:
            print(e)
            exc_type, exc_obj, exc_tb = sys.exc_info()
            logging.error("payload_creation :: ERR : -> Line:{} Exception:{}".format(exc_tb.tb_lineno, str(e)))

    def __on_open(self, ws):
        self.__ws_object = ws
        if self.on_open is not None:
            self.on_open()

    # def __on_close(self, ws, a, b):
    # 	# print("on_close")
    # 	# self.__ws_object = None
    # 	if self.__on_close is not None:
    # 		self.__ws_object = None

    def __on_error(self, ws, msg):
        if self.on_error is not None:
            self.on_error(msg)

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
                    'filename': os.path.join(self.log_path, 'fyers_socket.log')
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
