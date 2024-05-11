from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.decorators import api_view
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from django.core.exceptions import ObjectDoesNotExist

from applications.users.models import User
from applications.users.serializers import (
    UserSerializer,
    UserReadSerializer,
    UserUpdateSerializer
)
from applications.oauth.services.oauth2.decorators import oauth_permission
from applications.oauth.services.oauth2 import OAuth2Refresh
from config import OAUTH_SECRET_KEY


oauth = OAuth2Refresh(secret_key=OAUTH_SECRET_KEY)


@swagger_auto_schema(method='POST', request_body=UserSerializer, tags=["User"])
@api_view(['POST'])
def create_user(request: Request
                ) -> Response:
    user_serializer = UserSerializer(data=request.data)
    if user_serializer.is_valid():
        email = user_serializer.validated_data.get('email')
        password = user_serializer.validated_data.get('password')
        user = User(email=email, password=password)
        user.save()
        data_response = dict(user_serializer.data)
        data_response.update(id=user.pk)
        return Response(data_response, status=status.HTTP_201_CREATED)
    else:
        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(method='GET', tags=["User"])
@api_view(['GET'])
@oauth_permission(oauth)
def read_user(request: Request,
              user_id: int
              ) -> Response:
    try:
        user = User.objects.get(pk=user_id)
        serialized_clients = UserReadSerializer(data=user.__dict__)

        if serialized_clients.is_valid():
            return Response(serialized_clients.data, status=status.HTTP_200_OK)

        return Response(serialized_clients.errors, status=status.HTTP_400_BAD_REQUEST)
    except ObjectDoesNotExist:
        return Response({"Error": f"User not found"}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"Error": f"Unexpected error {e} occurred."}, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(method='GET', tags=["User"])
@api_view(['GET'])
@oauth_permission(oauth)
def read_users(request: Request
               ) -> Response:
    users = User.objects.all()

    serialized_clients = UserReadSerializer(data=list(users.values()), many=True)

    if serialized_clients.is_valid():
        return Response(serialized_clients.data, status=status.HTTP_200_OK)

    return Response(serialized_clients.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(method='PATCH', request_body=UserUpdateSerializer, tags=["User"])
@api_view(['PATCH'])
@oauth_permission(oauth)
def update_user(request: Request,
                user_id: int
                ) -> Response:
    try:
        user = User.objects.get(pk=user_id)
        update_serializer = UserUpdateSerializer(user, data=request.data, partial=True)
        if update_serializer.is_valid():
            update_serializer.save()
            return Response({"Message": "Client updated"}, status=status.HTTP_200_OK)
        else:
            return Response(update_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except ObjectDoesNotExist:
        return Response({"Error": f"User not found"}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"Error": f"Unexpected error {e} occurred."}, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(method='DELETE', tags=["User"])
@api_view(['DELETE'])
@oauth_permission(oauth)
def delete_user(request: Request,
                user_id: int
                ) -> Response:
    try:
        user = User.objects.get(pk=user_id)
        user.delete()
    except ObjectDoesNotExist:
        return Response({"Error": f"User not found"}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"Error": f"Unexpected error {e} occurred."}, status=status.HTTP_400_BAD_REQUEST)

    return Response({"Message": "Client have been deleted"}, status=status.HTTP_200_OK)
