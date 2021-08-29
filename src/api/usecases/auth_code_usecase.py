# Modules
from fyers_api import accessToken
from utils.data_classes import ReturnValue


class AuthCodeUseCase:
    def __init__(self, app_id, app_secret, redirect_url):
        self._app_id = app_id
        self._app_secret = app_secret
        self._redirect_url = redirect_url

        self._auth_code = None

    def generate_auth_code_url(self):
        response_type = "code"
        grant_type = "authorization_code"

        app_session = accessToken.SessionModel(
            client_id=self._app_id, redirect_uri=self._redirect_url, response_type=response_type, grant_type=grant_type,
            state="state", scope="", nonce=""
        )

        auth_code_url = app_session.generate_authcode()
        return ReturnValue(True, "Auth Code Url generated", data=auth_code_url)
