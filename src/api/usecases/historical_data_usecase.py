# Modules
from utils.helper import Helper
from constants.server_url import ServerUrl
from utils.data_classes import ReturnValue
from constants.redis_keys import RedisKeys
from db.redis_database import RedisDatabase


class HistoricalDataUseCase:
    def __init__(self, redis_database: RedisDatabase):
        self._redis_database = redis_database

    def get(
            self,
            symbol: str,
            resolution: str,
            range_from: str,
            range_to: str,
            date_format: int = 1,
            cont_flag: int = 1
    ) -> ReturnValue:

        url = ServerUrl.FYERS_HOST + ServerUrl.ENDPOINT_HISTORICAL_DATA
        payload = {
            "symbol": symbol,
            "resolution": resolution,
            "range_from": range_from,
            "range_to": range_to,
            "date_format": date_format,
            "cont_flag": cont_flag
        }
        authorization = self._redis_database.hget(RedisKeys.TOKENS, RedisKeys.AUTHORIZATION)
        if not authorization:
            return ReturnValue(False, "No authorization token found in redis")

        headers = {
            "User-Agent": "Mozilla/5.0",
            "Authorization": authorization
        }

        response = Helper.request_http_get(url, payload, headers)

        if response.status_code != 200:
            return ReturnValue(False, "Error while getting historical data",
                               error=response.reason, data=response.json())

        response_json = response.json()
        return ReturnValue(True, "Data found", data=response_json["candles"])
