# Packages
import traceback
from fastapi import APIRouter
from fastapi.responses import RedirectResponse

# Modules
from core import config
from utils.data_classes import ReturnValue
from api.usecases.auth_code_usecase import AuthCodeUseCase

router = APIRouter()

# AuthCode Usecase
auth_code_usecase = AuthCodeUseCase(config.APP_ID, config.APP_SECRET, config.REDIRECT_URL)


@router.get("/generate-auth-code")
async def generate_auth_code():
    try:
        result = auth_code_usecase.generate_auth_code_url()
        print(result)
        return RedirectResponse(result.data)

    except Exception as err:
        return ReturnValue(False, f"Error while generating auth code: {repr(err)}",
                           error=traceback.format_exc())
