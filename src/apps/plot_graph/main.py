# Packages
import pandas as pd
from typing import List
import mplfinance as mpf

# Modules
from core import config
from utils.helper import Helper
from constants.server_url import ServerUrl
from utils.data_classes import ReturnValue


class PlotGraph:
    def __init__(self, ta, symbol):
        self._ta = ta
        self._symbol = {
            "name": symbol,
            "df": {},
            "ema": {}
        }

    def request_chart_data(
            self,
            resolution: str,
            date_format: int,
            range_from: str,
            range_to: str,
    ):
        url = config.SERVER_URL + ServerUrl.ENDPOINT_HISTORICAL_DATA_API_SERVER
        payload = {
            "symbol": self._symbol["name"],
            "resolution": resolution,
            "range_from": range_from,
            "range_to": range_to,
            "date_format": date_format
        }
        response = Helper.request_http_get(url, payload)
        response_json = response.json()
        if not response_json["success"]:
            return ReturnValue(False, "Error requesting for historical data", error=response_json["error"])

        response_data = response_json["data"]

        chart_data = []

        for res in response_data:
            ohlc = [res[1], res[2], res[3], res[4]]
            volume = res[5]
            date = res[0]

            chart_data.append([date] + ohlc + [volume])

        symbol_df = pd.DataFrame(chart_data, columns=["date", "open", "high", "low", "close", "volume"])

        self._symbol["df"][resolution] = symbol_df

    def calculate_ema(self, resolution: str, ema_period: int):
        symbol_df = self._symbol["df"][resolution]
        ema_data = self._ta.EMA(symbol_df, adjust=False, period=ema_period)
        self._symbol["ema"][ema_period] = ema_data

    def plot_candlestick_chart(self, symbol: str, resolution: str, ema_periods: List[int]):
        ema_data = [{ema_period: self._symbol["ema"][ema_period]} for ema_period in ema_periods]

        symbol_df = self._symbol["df"][resolution]

        apd = []
        for ema in ema_data:
            # period = list(ema.keys())[0]
            data = list(ema.values())[0]

            apd.append(mpf.make_addplot(data))

        # apd = [mpf.make_addplot(ema, label=) for ema in ema_data]
        symbol_df = symbol_df.set_index("date")
        _datetime = pd.to_datetime(symbol_df.index, unit='s')
        symbol_df.index = _datetime.tz_localize('UTC').tz_convert("Asia/Kolkata")

        mpf.plot(
            symbol_df,
            type="candle",
            style="yahoo",
            title=symbol,
            ylabel="Price",
            ylabel_lower="Volume",
            figscale=1.5,
            addplot=apd,
            volume=True,
            # returnfig=True
        )
