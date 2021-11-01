# Packages
import sys
import pandas as pd
from time import sleep
from datetime import datetime, time

# Modules
from utils.helper import Helper
from utils.zmq_helper import ZMQSubscriber
from db.redis_database import RedisDatabase


class RangeBreakout:
    def __init__(self, redis_cli: RedisDatabase, zmq_subscriber: ZMQSubscriber):
        self._redis_cli = redis_cli
        self._zmq_subscriber = zmq_subscriber

        self._redis_pipe = self._redis_cli.pipeline
        self._zmq_subscriber_socket = None
        self._symbols_ohlc = {}

    def intialize(self):
        self._zmq_subscriber.connect()
        self._zmq_subscriber_socket = self._zmq_subscriber.get_socket()

    def _get_15_min_ohlc(self):
        symbols = self._redis_cli.keys("NSE:*")

        for symbol in symbols:
            symbol_data = self._redis_cli.hgetall(symbol)

            columns = ["timecode", "price", "volume"]
            rows = []

            for timecode, price_vol in symbol_data.items():
                d = Helper.convert_to_dict(price_vol)
                price = d["price"]
                vol = d["volume"]

                rows.append([timecode, price, vol])

            df = pd.DataFrame(rows, columns=columns)
            df.set_index("timecode", inplace=True)
            df.index = pd.to_datetime(df.index)
            df.sort_values(by="timecode", inplace=True)
            price = df["price"]

            s_range = Helper.get_current_time_in_str("%Y-%m-%d 09:15:00")
            e_range = Helper.get_current_time_in_str("%Y-%m-%d 09:29:59")
            first_candle = price[s_range:e_range]
            ohlc = first_candle.resample("15min").ohlc()

            self._symbols_ohlc[symbol] = {
                "open": float(ohlc.open),
                "high": float(ohlc.high),
                "low": float(ohlc.low),
                "close": float(ohlc.close),
                "is_high_break": False,
                "is_low_break": False
            }

    def _check_range_breakout(self, feed):
        if datetime.now().time() >= time(16, 5):
            print("Trading hours ended! Exiting...")
            sys.exit()

        for f in feed:
            ltp = f["ltp"]
            symbol = f["symbol"]
            timestamp = f["timestamp"]
            date_time = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

            ohlc = self._symbols_ohlc[symbol]

            if ltp > ohlc["high"] and ohlc["is_high_break"] is False:
                print(f"{symbol}: {date_time} (High break)")
                self._symbols_ohlc[symbol]["is_high_break"] = True

            if ltp < ohlc["low"] and ohlc["is_low_break"] is False:
                print(f"{symbol}: {date_time} (Low break)")
                self._symbols_ohlc[symbol]["is_low_break"] = True

    def wait_for_time_to_start(self):
        current_time = Helper.get_current_time()
        till_time = datetime(current_time.year, current_time.month, current_time.day,
                             9, 30, 1)
        wait_time = (till_time - current_time).total_seconds()
        print(f"Service will start at {till_time}")
        sleep(wait_time)
        print("Service Started!")

    def run(self):
        self._get_15_min_ohlc()
        while True:
            msg = self._zmq_subscriber_socket.recv_string()
            feed = Helper.convert_to_dict(msg)
            self._check_range_breakout(feed)
