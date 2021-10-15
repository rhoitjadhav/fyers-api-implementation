# Packages
import sys
from finta.finta import TA
from datetime import timedelta

# Modules
from core import config
from utils.helper import Helper
from apps.plot_graph.main import PlotGraph
from db.redis_database import RedisDatabase
from apps.market_feed.main import MarketFeed
from apps.store_intraday_ohlc.main import StoreIntradayOHLC


def market_feed(symbols):
    mf = MarketFeed(symbols, config.APP_ID, config.SERVER_URL)
    mf.start_feed(mf.print_symbol_feed)


def plot_graph(symbol):
    current_date = Helper.get_current_time()
    resolution = "15"
    date_format = 1
    range_from = (current_date - timedelta(days=20)).strftime("%Y-%m-%d")  # "2020-10-02"
    range_to = current_date.strftime("%Y-%m-%d")  # "2021-10-01"
    ema_period_10 = 10
    ema_period_20 = 20
    ema_period_50 = 50
    ema_period_100 = 100
    ema_period_200 = 200

    pg = PlotGraph(TA, symbol)
    pg.request_chart_data(resolution, date_format, range_from, range_to)
    pg.calculate_ema(resolution, ema_period_10)
    pg.calculate_ema(resolution, ema_period_20)
    pg.calculate_ema(resolution, ema_period_50)
    pg.calculate_ema(resolution, ema_period_100)
    pg.calculate_ema(resolution, ema_period_200)
    pg.plot_candlestick_chart(symbol, resolution, [ema_period_50, ema_period_200])


def store_intraday_ohlc(symbols):
    redis_cli = RedisDatabase()
    s = StoreIntradayOHLC(config.SERVER_URL, symbols, redis_cli)
    s.fetch_access_authorization()
    s.initialize()
    s.run()


args = sys.argv

if len(args) < 2:
    print("Too less parameters")
    sys.exit()

if args[1] in {"market_feed", "store_intraday_ohlc"}:
    _args = args[2].split(",")
    func = globals()[args[1]]
    func(_args)

elif args[1] in {"plot_graph"}:
    _args = args[2]
    func = globals()[args[1]]
    func(_args)

else:
    print(f"Invalid Arguements: {args[1:]}")
