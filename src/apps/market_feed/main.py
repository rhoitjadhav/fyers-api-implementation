# Packages
import traceback
from typing import List
from fyers_api.Websocket.ws import FyersSocket

# Modules
from utils.helper import Helper
from utils.zmq_helper import ZMQPublisher
from constants.server_url import ServerUrl
from utils.data_classes import ReturnValue
from db.redis_database import RedisDatabase
from utils.fyers_api_helper import FyersApiHelper


class MarketFeed(FyersSocket):
    def __init__(self, server_url, symbols: List[str], redis_cli: RedisDatabase, zmq_publisher: ZMQPublisher):
        self._server_url = server_url
        self._redis_cli = redis_cli
        self._zmq_publisher = zmq_publisher

        self._redis_pipe = self._redis_cli.pipeline
        self._zmq_publisher_socket = None
        self._access_authorization = None
        self._data_type = "symbolData"
        self._symbols = symbols

        FyersSocket.websocket_data = self.publish_feed

    def initialize(self):
        super().__init__(self._access_authorization, self._data_type, self._symbols)
        self._zmq_publisher.connect()

    def fetch_access_authorization(self) -> ReturnValue:
        url = self._server_url + ServerUrl.ENDPOINT_TOKENS_API_SERVER

        response = Helper.request_http_get(url, None)
        if response.status_code != 200:
            return ReturnValue(False, "Error while getting access authorization", error=response.reason)

        response = response.json()
        if response["success"]:
            self._access_authorization = response["data"]["authorization"]
            return ReturnValue(True, data=self._access_authorization)

        return ReturnValue(False, response["message"], error=response["error"])

    def publish_feed(self):
        try:
            feed = Helper.convert_to_json(self.response)
            self._zmq_publisher.send_msg(feed)
        except Exception as _:
            print(traceback.print_exc())

    def run(self):
        print(f"Started Feed for {self._symbols}")
        self.subscribe()


class MarketFeedNew:
    def __init__(
            self,
            fyers_api_helper: FyersApiHelper,
            zmq_publisher: ZMQPublisher
    ):
        self._fyers_api_helper = fyers_api_helper
        self._zmq_publisher = zmq_publisher

    def initialize(self):
        self._zmq_publisher.connect()

    def publish_feed(self, feed):
        try:
            _feed = Helper.convert_to_json(feed)
            self._zmq_publisher.send_msg(_feed)

        except Exception as _:
            print(traceback.print_exc())

    def run(self):
        self._fyers_api_helper.start_stream(self.publish_feed)
