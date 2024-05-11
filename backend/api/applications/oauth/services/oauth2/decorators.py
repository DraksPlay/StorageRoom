from typing import Callable
from rest_framework.request import Request
from rest_framework import status
from django.http import HttpResponse

from .applications import OAuth2Refresh


def oauth_permission(oauth: OAuth2Refresh):

    def decorator(func: Callable):

        def wrapper(*args, **kwargs):
            request: Request = args[0]

            token = request.headers.get('Authorization', False)

            if not token:
                return HttpResponse(status=status.HTTP_403_FORBIDDEN)

            payload = oauth.get_payload(token)
            user_id = payload.get("user_id", False)
            if not user_id:
                return HttpResponse(status=status.HTTP_403_FORBIDDEN)

            res = func(*args, **kwargs)
            return res

        return wrapper

    return decorator
