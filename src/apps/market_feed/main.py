# Packages
import requests
from datetime import datetime

# Modules
from utils.data_classes import ReturnValue
from constants.server_url import ServerUrl
from fyers_api.websocket.ws import FyersSocket


class MarketFeed:
    def __init__(self, symbols, app_id, server_url):
        self._symbols = symbols
        self._app_id = app_id
        self._server_url = server_url

        self._access_token = None
        self._access_authorization = None
        self._fyers_socket = None

    def _get_access_authorization(self):
        if self._access_authorization:
            return self._access_authorization

        # Request API server for access token
        url = self._server_url + ServerUrl.ENDPOINT_TOKENS_API_SERVER

        response = requests.get(url)
        if response.status_code != 200:
            return ReturnValue(False, "Error while getting access authorization", error=response.reason)

        response = response.json()
        if response["success"]:
            return ReturnValue(True, data=response["data"]["authorization"])

        return ReturnValue(False, "Error while getting access authorization", error=response["error"])

    @staticmethod
    def print_symbol_feed(feed):
        for r in feed.response:
            t = datetime.fromtimestamp(r['last_traded_time']).strftime("%Y-%m-%d %H:%M:%S")
            ltt = f"LTT: {t}"
            ltp = f"LTP: {r['ltp']}"
            sym = f"{r['symbol']}"
            vol = f"Vol: {r['vol_traded_today']}"
            bqt = f"Bqt: {r['tot_buy_qty']}"
            msg = f"  {sym}-> {ltp}, {vol}, {ltt}, {bqt}"
            print(msg, end="\r")

    def start_feed(self, feed_caputring_object):
        access_authorization = self._get_access_authorization().data
        if not access_authorization:
            return_value = ReturnValue(False, "Access Authorization not found")
            print(return_value)
            return

        data_type = "symbolData"

        FyersSocket.websocket_data = feed_caputring_object

        print(f"Feed Started for symbols: {self._symbols}")
        self._fyers_socket = FyersSocket(access_token=access_authorization, data_type=data_type, symbol=self._symbols)
        self._fyers_socket.subscribe()
