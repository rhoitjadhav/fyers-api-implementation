# Packages
import traceback
from starlette import status
from fastapi import APIRouter
from fastapi.responses import Response

# Modules
from core import config
from utils.data_classes import ReturnValue
from api.usecases.access_token_usecase import AccessTokenUseCase

router = APIRouter()

access_token_usecase = AccessTokenUseCase(config.APP_ID, config.APP_SECRET, config.REDIRECT_URL)


@router.get("/generate-access-token")
async def generate_access_token(
        response: Response,
        s: str,
        code: str,
        auth_code: str,
        state: str
):
    try:
        return_value = access_token_usecase.generate_access_token(auth_code)
        return ReturnValue(True, "Access Token Generated", data={
            "status": s,
            "status_code": code,
            "auth_code": auth_code,
            "state": state,
            "access_token": return_value.data
        })

    except Exception as err:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return ReturnValue(False, f"Error while generating access token: {repr(err)}",
                           error=traceback.format_exc())


@router.get("/access-token")
def access_token(response: Response):
    try:
        _access_token = access_token_usecase.access_token
        if _access_token:
            return ReturnValue(True, "Access Token found", data=_access_token)

        return ReturnValue(False, "Access Token not found", data="")

    except Exception as err:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return ReturnValue(False, f"Error while getting access token: {repr(err)}",
                           error=traceback.format_exc())
