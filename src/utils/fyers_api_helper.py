# Packages
from fyers_api.Websocket.ws import FyersSocket


class FyersApiHelper(FyersSocket):
    def __init__(
            self,
            symbols,
            access_authorization: str,
            run_background: bool = False,
            log_path: str = "",
            data_type: str = "symbolData",
    ):
        self._symbols = symbols
        self._data_type = data_type
        self._access_authorization = access_authorization
        super().__init__(access_token=access_authorization,
                         run_background=run_background,
                         log_path=log_path)
        self.websocket_data = self.msg

    def msg(self, feed):
        print(feed)

    def start_stream(self, msg=None):
        if msg:
            self.websocket_data = msg

        print(f"Market Feed Started for {self._symbols}")
        self.subscribe(symbol=self._symbols, data_type=self._data_type)
