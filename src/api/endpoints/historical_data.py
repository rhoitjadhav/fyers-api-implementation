# Packages
import traceback
from starlette import status
from fastapi import APIRouter
from fastapi.responses import Response

# Modules
from core import config
from utils.data_classes import ReturnValue
from db.redis_database import RedisDatabase
from api.usecases.historical_data_usecase import HistoricalDataUseCase

router = APIRouter()

redis_database = RedisDatabase(config.REDIS_HOST, config.REDIS_PORT, config.REDIS_DB)
historical_data_usecase = HistoricalDataUseCase(redis_database)


@router.get("/historical-data")
async def get_historical_data(
        response: Response,
        symbol: str,
        resolution: str,
        range_from: str,
        range_to: str,
        date_format: int = 1,
        cont_flag: int = 1
):
    try:
        return historical_data_usecase.get(symbol, resolution, range_from, range_to, date_format, cont_flag)

    except Exception as err:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return ReturnValue(False, f"Error while generating access token: {repr(err)}",
                           error=traceback.format_exc())
