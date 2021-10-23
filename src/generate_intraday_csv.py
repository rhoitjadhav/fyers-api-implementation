import sys
import json
import pandas as pd
from db.redis_database import RedisDatabase

r = RedisDatabase()

symbol = sys.argv[1]
filename = sys.argv[2]

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

df.to_csv(filename, header=True)
