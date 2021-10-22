# Packages
import sys
import json
import requests
from typing import List
from datetime import datetime, time
from fyers_api.websocket.ws import FyersSocket

# Modules
from constants.server_url import ServerUrl
from utils.data_classes import ReturnValue
from db.redis_database import RedisDatabase


class StoreIntradayOHLC(FyersSocket):
    def __init__(self, server_url, symbols: List[str], redis_cli: RedisDatabase):
        self._server_url = server_url
        self._redis_cli = redis_cli
        self._redis_pipe = self._redis_cli.pipeline
        self._access_authorization = None
        self._data_type = "symbolData"
        self._symbols = symbols

        FyersSocket.websocket_data = self.store_feed

    def initialize(self):
        super().__init__(self._access_authorization, self._data_type, self._symbols)

    def fetch_access_authorization(self) -> ReturnValue:
        url = self._server_url + ServerUrl.ENDPOINT_TOKENS_API_SERVER

        response = requests.get(url)
        if response.status_code != 200:
            return ReturnValue(False, "Error while getting access authorization", error=response.reason)

        response = response.json()
        if response["success"]:
            self._access_authorization = response["data"]["authorization"]
            return ReturnValue(True, data=self._access_authorization)

        return ReturnValue(False, response["message"], error=response["error"])

    def store_feed(self):
        if datetime.now().time() >= time(16, 5):
            print("Trading hours ended! Exiting...")
            sys.exit()

        for r in self.response:
            symbol = r["symbol"]
            timestamp = r["timestamp"]
            ltp = r["ltp"]
            volume = r["vol_traded_today"]

            name = symbol
            key = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
            value = json.dumps({
                "price": ltp,
                "volume": volume
            })

            self._redis_pipe.hset(name, key, value)

        self._redis_pipe.execute()

    def run(self):
        print(f"Started Feed for {self._symbols}")
        self.subscribe()
