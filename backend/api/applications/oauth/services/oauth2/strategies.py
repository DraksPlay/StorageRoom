import datetime
import jwt

from .enums import Algorithms


class AuthStrategy:

    def __init__(self,
                 secret_key: str,
                 algorithm: Algorithms,
                 *args,
                 **kwargs
                 ) -> None:
        self._secret_key = secret_key
        self._algorithm = algorithm
        self._decode_error = None

    @property
    def decode_error(self):
        return self._decode_error

    def create_token(self,
                     payload: dict | None = None,
                     **kwargs
                     ) -> dict:
        if payload is None:
            payload = dict(kwargs)

        payload["iat"] = datetime.datetime.utcnow()

        return {"access_token": self._encode_jwt(payload)}

    def check_token(self,
                    token: str,
                    ):
        check_data = self._decode_jwt(token)

        result = {}

        if not check_data:
            result['status'] = True
        else:
            result['status'] = False
            result['error'] = self.decode_error

        return check_data

    def get_payload_from_token(self,
                               token: str,
                               ) -> dict | bool:
        payload = self._decode_jwt(token)

        return payload

    def _encode_jwt(self,
                    payload: dict
                    ) -> str:
        token = jwt.encode(payload, self._secret_key, algorithm=self._algorithm.value)

        return token

    def _decode_jwt(self,
                    token: str
                    ) -> dict | bool:
        try:
            payload = jwt.decode(token, self._secret_key, algorithms=[self._algorithm.value])
        except Exception as exc:
            self._decode_error = exc

            return False
        else:
            self._decode_error = None

            return payload


class OAuth2Strategy(AuthStrategy):

    def __init__(self,
                 secret_key: str,
                 algorithm: Algorithms,
                 access_token_expiration: datetime.timedelta,
                 ) -> None:
        super().__init__(secret_key, algorithm)
        self._access_token_expiration = access_token_expiration

    def create_token(self,
                     payload: dict | None = None,
                     **kwargs
                     ) -> dict:
        if payload is None:
            payload = dict(kwargs)

        payload["exp"] = datetime.datetime.utcnow() + self._access_token_expiration

        return {"access_token": super(AuthStrategy).create_token(payload)}


class OAuth2RefreshStrategy(AuthStrategy):

    def __init__(self,
                 secret_key: str,
                 algorithm: Algorithms,
                 access_token_expiration: datetime.timedelta,
                 refresh_token_expiration: datetime.timedelta,
                 ) -> None:
        super().__init__(secret_key, algorithm)
        self._access_token_expiration = access_token_expiration
        self._refresh_token_expiration = refresh_token_expiration

    def create_token(self,
                     payload: dict | None = None,
                     **kwargs
                     ) -> dict:
        if payload is None:
            payload_access = dict(kwargs)
            payload_refresh = dict(kwargs)
        else:
            payload_access = dict(payload)
            payload_refresh = dict(payload)

        payload_access["exp"] = datetime.datetime.utcnow() + self._access_token_expiration
        payload_refresh["exp"] = datetime.datetime.utcnow() + self._refresh_token_expiration

        access_token = super(OAuth2RefreshStrategy, self).create_token(payload_access).get("access_token")
        refresh_token = super(OAuth2RefreshStrategy, self).create_token(payload_refresh).get("access_token")

        return {"access_token": access_token, "refresh_token": refresh_token}
