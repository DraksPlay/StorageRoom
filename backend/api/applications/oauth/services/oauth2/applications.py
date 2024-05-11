import datetime

from .strategies import (
    OAuth2Strategy,
    OAuth2RefreshStrategy
)
from .core import OAuth2Core
from .enums import Algorithms


class OAuth2:

    def __init__(self,
                 secret_key: str,
                 algorithm: Algorithms = Algorithms.HS256,
                 access_token_expiration: datetime.timedelta = datetime.timedelta(minutes=15)
                 ) -> None:
        self._secret_key = secret_key
        self._algorithm = algorithm
        self._access_token_expiration = access_token_expiration
        self._strategy = OAuth2Strategy(secret_key, algorithm, access_token_expiration)
        self._core = OAuth2Core(self._strategy)

    def create_token(self,
                     payload: dict | None = None
                     ) -> str:
        access_token = self._core.create_token(payload=payload).get("access_token")

        return access_token

    def check_token(self,
                    token: str
                    ) -> dict:
        check_data = self._core.check_token(token)

        return check_data

    def get_payload(self,
                    token: str
                    ) -> dict | bool:
        payload = self._core.get_payload(token)

        return payload


class OAuth2Refresh:

    def __init__(self,
                 secret_key: str,
                 algorithm: Algorithms = Algorithms.HS256,
                 access_token_expiration: datetime.timedelta = datetime.timedelta(minutes=15),
                 refresh_token_expiration: datetime.timedelta = datetime.timedelta(days=15)
                 ) -> None:
        self._secret_key = secret_key
        self._algorithm = algorithm
        self._access_token_expiration = access_token_expiration
        self._refresh_token_expiration = refresh_token_expiration
        self._strategy = OAuth2RefreshStrategy(secret_key, algorithm, access_token_expiration, refresh_token_expiration)
        self._core = OAuth2Core(self._strategy)

    def create_tokens(self,
                      payload: dict | None = None
                      ) -> tuple[str, str]:
        token_data = self._core.create_token(payload=payload)
        access_token = token_data.get("access_token")
        refresh_token = token_data.get("refresh_token")

        return access_token, refresh_token

    def check_token(self,
                    token: str
                    ) -> dict:
        check_data = self._core.check_token(token)

        return check_data

    def get_payload(self,
                    token: str
                    ) -> dict | bool:
        payload = self._core.get_payload(token)

        return payload
