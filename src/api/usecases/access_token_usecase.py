# Modules
from utils.data_classes import ReturnValue
from fyers_api.accessToken import SessionModel


class AccessTokenUseCase:
    def __init__(self, app_id, app_secret, redirect_url):
        self._app_id = app_id
        self._app_secret = app_secret
        self._redirect_url = redirect_url

        self._access_token = None

    @property
    def access_token(self):
        return self._access_token

    def generate_access_token(self, auth_code: str) -> ReturnValue:
        grant_type = "authorization_code"
        app_session = SessionModel(client_id=self._app_id, secret_key=self._app_secret, grant_type=grant_type)

        app_session.set_token(auth_code)
        response = app_session.generate_token()
        self._access_token = response["access_token"]
        return ReturnValue(True, "Access Token Generated", data=self._access_token)
