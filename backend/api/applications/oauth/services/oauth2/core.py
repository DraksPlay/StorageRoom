from .strategies import AuthStrategy


class OAuth2Core:

    def __init__(self,
                 strategy: AuthStrategy
                 ) -> None:
        self._strategy = strategy

    @property
    def strategy(self) -> AuthStrategy:
        return self._strategy

    def create_token(self,
                     payload: dict | None = None,
                     ) -> dict:
        return self._strategy.create_token(payload=payload)

    def check_token(self,
                    token: str
                    ) -> dict:
        return self._strategy.check_token(token)

    def get_payload(self,
                    token: str
                    ) -> dict | bool:
        return self._strategy.get_payload_from_token(token)
