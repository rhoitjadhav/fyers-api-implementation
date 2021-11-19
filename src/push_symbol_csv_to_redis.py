import pandas as pd
from utils.helper import Helper
from db.redis_database import RedisDatabase

r = RedisDatabase()

df = pd.read_csv("symbols_feed_data/l&t_26Oct2021.csv")

name = "NSE:LT-EQ"
for d in df.to_numpy():
    timecode = d[0]
    price = d[1]
    volume = d[2]

    value = Helper.convert_to_json({"price": price, "volume": volume})
    r.pipeline.hset(name, timecode, value)

r.pipeline.execute()
