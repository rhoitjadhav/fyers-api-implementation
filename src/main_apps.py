# Packages
import sys
from finta.finta import TA
from datetime import timedelta

# Modules
from core import config
from utils.helper import Helper
from apps.bod_task.main import BODTask
from constants.server_url import ServerUrl
from apps.plot_graph.main import PlotGraph
from utils.data_classes import ReturnValue
from db.redis_database import RedisDatabase
from apps.market_feed.main import MarketFeed, MarketFeedNew
from utils.fyers_api_helper import FyersApiHelper
from apps.range_breakout.main import RangeBreakout
from utils.zmq_helper import ZMQPublisher, ZMQSubscriber
from apps.store_market_feed.main import StoreMarketFeed, StoreMarketFeedZmqSub


def _fetch_access_authorization():
    url = config.API_SERVER_URL + ServerUrl.ENDPOINT_TOKENS_API_SERVER

    response = Helper.request_http_get(url, None)
    if response.status_code != 200:
        return ReturnValue(False, "Error while getting access authorization", error=response.reason)

    response = response.json()
    if response["success"]:
        access_authorization = response["data"]["authorization"]
        return ReturnValue(True, data=access_authorization)

    return ReturnValue(False, response["message"], error=response["error"])


def market_feed(symbols):
    r = RedisDatabase()
    z = ZMQPublisher("*", config.ZMQ_PORT)
    mf = MarketFeed(config.API_SERVER_URL, symbols, r, z)
    result = mf.fetch_access_authorization()
    if not result.success:
        print(f"\n{result}")
        return
    mf.initialize()
    mf.run()


def market_feed_new(symbols):
    z = ZMQPublisher("*", config.ZMQ_PORT)
    result = _fetch_access_authorization()
    if not result.success:
        print(result)
        return

    access_authorization = result.data
    fah = FyersApiHelper(symbols, access_authorization, log_path="./")
    mf1 = MarketFeedNew(fah, z)
    mf1.initialize()
    mf1.run()


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
    s = StoreMarketFeed(config.API_SERVER_URL, symbols, redis_cli)
    result = s.fetch_access_authorization()
    if not result.success:
        print(f"\n{result}")
        return
    s.initialize()
    s.run()


def store_feed_zmq_sub():
    r = RedisDatabase()
    z = ZMQSubscriber(config.ZMQ_HOST, config.ZMQ_PORT)
    s = StoreMarketFeedZmqSub(z, r)
    s.intialize()
    s.run()


def bod_task():
    r = RedisDatabase()
    b = BODTask(config.FYERS_USERNAME, config.FYERS_PASSWORD, config.PAN_ID, r, config.API_SERVER_URL)
    b.redis_flush_db()
    b.generate_auth_code()


def range_breakout():
    r = RedisDatabase()
    z = ZMQSubscriber(config.ZMQ_HOST, config.ZMQ_PORT)
    rb = RangeBreakout(r, z)
    rb.wait_for_time_to_start()
    rb.intialize()
    rb.run()


args = sys.argv

if len(args) < 2:
    print("Too less parameters")
    sys.exit()

if args[1] in {"store_market_feed", "market_feed", "market_feed_new"}:
    _args = args[2].split(", ")
    func = globals()[args[1]]
    func(_args)

elif args[1] in {"plot_graph"}:
    _args = args[2]
    func = globals()[args[1]]
    func(_args)

elif args[1] in {"bod_task", "store_feed_zmq_sub", "range_breakout"}:
    func = globals()[args[1]]
    func()

else:
    print(f"Invalid Arguements: {args[1:]}")
