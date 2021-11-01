# Packages
import sys
import json
import pandas as pd
from datetime import datetime

# Modules
from utils.helper import Helper
from db.redis_database import RedisDatabase

r = RedisDatabase()

symbol = sys.argv[1]
filename = sys.argv[2] + "_" + Helper.get_current_time_in_str("%d%b%Y.csv")

timeseries_data = r.hgetall(symbol)

columns = ["timecode", "price", "volume"]
rows = []

for timecode, price_vol in timeseries_data.items():
    d = json.loads(price_vol)
    price = d["price"]
    vol = d["volume"]

    rows.append([timecode, price, vol])

df = pd.DataFrame(rows, columns=columns)
df.set_index("timecode", inplace=True)
df.index = pd.to_datetime(df.index)

df.to_csv(f"symbols_feed_data/{filename}", header=True)
