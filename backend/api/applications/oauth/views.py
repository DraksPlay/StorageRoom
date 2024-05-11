from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.decorators import api_view
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from django.core.exceptions import ObjectDoesNotExist

from applications.users.models import User
from applications.oauth.models import Token
from applications.oauth.serializers import (
    TokenSerializer,
    TokenUpdateSerializer,
    SignInSerializer,
    CheckAuthSerializer
)
from applications.oauth.services.oauth2 import OAuth2Refresh
from config import OAUTH_SECRET_KEY


oauth = OAuth2Refresh(secret_key=OAUTH_SECRET_KEY)


@swagger_auto_schema(method='POST', request_body=TokenSerializer, tags=["Auth"])
@api_view(['POST'])
def create_tokens(request: Request
                  ) -> Response:
    token_serializer = TokenSerializer(data=request.data)
    if token_serializer.is_valid():
        user_id = token_serializer.validated_data.get('user_id')
        payload = {"user_id": user_id}
        access_token, refresh_token = oauth.create_tokens(payload=payload)
        token_obj = Token(refresh_token=refresh_token)
        token_obj.save()
        data_response = {"access_token": access_token, "refresh_token": refresh_token}

        return Response(data_response, status=status.HTTP_201_CREATED)
    else:
        return Response(token_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(method='PUT', request_body=TokenUpdateSerializer, tags=["Auth"])
@api_view(['PUT'])
def update_tokens(request: Request,
                  ) -> Response:
    try:
        update_serializer = TokenUpdateSerializer(data=request.data)
        if update_serializer.is_valid():
            refresh_token = update_serializer.validated_data.get('refresh_token')
            token_obj = Token.objects.get(refresh_token=refresh_token)
            payload = oauth.get_payload(token_obj.refresh_token)
            payload = dict(user_id=payload['user_id'])
            access_token, refresh_token = oauth.create_tokens(payload=payload)
            data_response = {"access_token": access_token, "refresh_token": refresh_token}
            token_obj.refresh_token = refresh_token
            token_obj.save()

            return Response(data_response, status=status.HTTP_200_OK)
        else:
            return Response(update_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except ObjectDoesNotExist:
        return Response({"Error": f"Token not found"}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"Error": f"Unexpected error {e} occurred."}, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(method='POST', request_body=SignInSerializer, tags=["Auth"])
@api_view(['POST'])
def sign_in(request: Request
            ) -> Response:
    try:
        sign_in_serializer = SignInSerializer(data=request.data)
        if sign_in_serializer.is_valid():
            email = sign_in_serializer.validated_data.get('email')
            password = sign_in_serializer.validated_data.get('password')
            user = User.objects.get(email=email)

            if user.password != password:
                return Response({"Error": f"Password invalid"}, status=status.HTTP_400_BAD_REQUEST)

            payload = {"user_id": user.id}
            access_token, refresh_token = oauth.create_tokens(payload=payload)
            token_obj = Token(refresh_token=refresh_token)
            token_obj.save()
            data_response = {"access_token": access_token, "refresh_token": refresh_token}

            return Response(data_response, status=status.HTTP_200_OK)
        else:
            return Response(sign_in_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except ObjectDoesNotExist:
        return Response({"Error": f"User not found"}, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(method='POST', request_body=CheckAuthSerializer, tags=["Auth"])
@api_view(['POST'])
def check_auth(request: Request
               ) -> Response:
    try:
        check_auth_serializer = CheckAuthSerializer(data=request.data)
        if check_auth_serializer.is_valid():
            access_token = check_auth_serializer.validated_data.get('access_token')
            oauth_data = oauth.check_token(access_token)
            if not oauth_data.get("status", False):
                return Response(status=status.HTTP_403_FORBIDDEN)

            return Response(status=status.HTTP_200_OK)
        else:
            return Response(check_auth_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except ObjectDoesNotExist:
        return Response({"Error": f"User not found"}, status=status.HTTP_400_BAD_REQUEST)
