# Packages
import requests
from datetime import datetime

# Modules
from utils.data_classes import ReturnValue
from fyers_api.websocket.ws import FyersSocket


def _print_symbol_feed(self):
    print(self.response)


class MarketFeed:
    def __init__(self, symbols, app_id, server_url):
        self._symbols = symbols
        self._app_id = app_id
        self._server_url = server_url

        self._access_token = None
        self._fyers_socket = None

    def _get_access_token(self):
        if self._access_token:
            return self._access_token

        # Request API server for access token
        url = self._server_url + "/access-token"

        response = requests.get(url)
        if response.status_code != 200:
            return ReturnValue(False, "Error while getting access token", error=response.reason)

        response = response.json()
        if response["success"]:
            return ReturnValue(True, data=response["data"])

        return ReturnValue(False, "Error while getting access token", error=response["error"])

    @staticmethod
    def _print_symbol_feed(feed):
        # print(feed.response)
        for r in feed.response:
            t = datetime.fromtimestamp(r['last_traded_time']).strftime("%Y-%m-%d %H:%M:%S")
            ltt = f"LTT: {t}"
            ltp = f"LTP: {r['ltp']}"
            sym = f"{r['symbol']}"
            vol = f"Vol: {r['vol_traded_today']}"
            bqt = f"Bqt: {r['tot_buy_qty']}"
            msg = f"  {sym}-> {ltp}, {vol}, {ltt}, {bqt}"
            print(msg, end="\r")

    def start_feed(self):
        access_token = self._get_access_token().data
        if not access_token:
            return_value = ReturnValue(False, "Token not found")
            print(return_value)
            return

        _access_token = f"{self._app_id}:{access_token}"
        data_type = "symbolData"

        FyersSocket.websocket_data = self._print_symbol_feed

        print(f"Feed Started for symbols: {self._symbols}")
        self._fyers_socket = FyersSocket(access_token=_access_token, data_type=data_type, symbol=self._symbols)
        self._fyers_socket.subscribe()
