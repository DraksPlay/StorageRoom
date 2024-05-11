from typing import Callable
from django.http import HttpRequest, HttpResponse


class AuthMiddleware:

    def __init__(self,
                 get_response: Callable
                 ) -> None:
        self.get_response = get_response

    def __call__(self,
                 request: HttpRequest
                 ) -> HttpResponse:
        access_token = request.headers.get("Authorization")


        response = self.get_response(request)

        return response
