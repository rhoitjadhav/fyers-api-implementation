# Modules
from utils.data_classes import ReturnValue
from constants.redis_keys import RedisKeys
from db.redis_database import RedisDatabase
from fyers_api.accessToken import SessionModel


class AccessTokenUseCase:
    def __init__(self, app_id: str, app_secret: str, redirect_url: str, redis_database: RedisDatabase):
        self._app_id = app_id
        self._app_secret = app_secret
        self._redirect_url = redirect_url
        self._redis_database = redis_database
        self._access_token = None

    @property
    def access_token(self):
        return self._access_token

    @property
    def app_id(self):
        return self._app_id

    def generate_access_token(self, auth_code: str) -> ReturnValue:
        grant_type = "authorization_code"
        app_session = SessionModel(client_id=self._app_id, secret_key=self._app_secret, grant_type=grant_type)

        app_session.set_token(auth_code)
        response = app_session.generate_token()
        self._access_token = response["access_token"]

        # Save tokens to Redis
        mapping = {
            RedisKeys.ACCESS_TOKEN: self._access_token,
            RedisKeys.AUTHORIZATION: f"{self._app_id}:{self._access_token}"
        }
        self._redis_database.hset(RedisKeys.TOKENS, mapping=mapping)

        return ReturnValue(True, "Access Token Generated", data=self._access_token)

    def get_tokens(self):
        if not self._access_token:
            return ReturnValue(False, "Tokens not found")

        data = {
            "app_id": self._app_id,
            "access_token": self._access_token,
            "authorization": f"{self._app_id}:{self._access_token}"
        }
        return ReturnValue(True, "Tokens found", data=data)

    def get_tokens_from_redis(self):
        tokens = self._redis_database.hgetall(RedisKeys.TOKENS)

        if not tokens:
            return ReturnValue(False, "Need to generate tokens first")

        access_token = tokens[RedisKeys.ACCESS_TOKEN]
        data = {
            "app_id": self._app_id,
            "access_token": access_token,
            "authorization": f"{self._app_id}:{access_token}"
        }
        return ReturnValue(True, "Tokens found from redis", data=data)
