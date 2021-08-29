# Packages
import sys

# Modules
from core import config
from apps.market_feed.main import MarketFeed


def market_feed(symbols):
    mf = MarketFeed(symbols, config.APP_ID, config.SERVER_URL)
    mf.start_feed()


args = sys.argv

if len(args) < 2:
    print("Too less parameters")
    sys.exit()

if args[1] == "market_feed":
    _symbols = args[2].split(",")
    market_feed(_symbols)
else:
    print(f"Invalid Arguements: {args[1:]}")
