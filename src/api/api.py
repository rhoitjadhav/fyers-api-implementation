# Packages
from fastapi import APIRouter

# Modules
from .endpoints.auth_code import router as auth_code_router
from .endpoints.historical_data import router as historical_data
from .endpoints.access_token import router as generate_access_token_router

router = APIRouter()

router.include_router(auth_code_router)
router.include_router(historical_data)
router.include_router(generate_access_token_router)
