from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.decorators import api_view
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from django.core.exceptions import ObjectDoesNotExist

from applications.storages.models import (
    Storage,
    Category
)
from applications.storages.serializers import (
    StorageSerializer,
    StorageReadSerializer,
)
from applications.users.models import User


@swagger_auto_schema(method='POST', request_body=StorageSerializer, tags=["Storage"])
@api_view(['POST'])
def create_storage(request: Request
                   ) -> Response:
    storage_serializer = StorageSerializer(data=request.data)
    if storage_serializer.is_valid():
        user_id = storage_serializer.validated_data.get('user_id')
        category_id = storage_serializer.validated_data.get('category_id')
        price = storage_serializer.validated_data.get('price')
        start_at = storage_serializer.validated_data.get('start_at')
        finish_at = storage_serializer.validated_data.get('finish_at')

        try:
            user = User.objects.get(pk=user_id)
        except ObjectDoesNotExist:
            return Response("User not found", status=status.HTTP_400_BAD_REQUEST)

        try:
            category = Category.objects.get(pk=category_id)
        except ObjectDoesNotExist:
            return Response("Category not found", status=status.HTTP_400_BAD_REQUEST)

        storage = Storage(user=user, category=category, price=price, start_at=start_at, finish_at=finish_at)
        storage.save()
        return Response(storage_serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(storage_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(method='GET', tags=["Storage"])
@api_view(['GET'])
def read_storage(request: Request,
                 storage_id: int
                 ) -> Response:
    try:
        storage = Storage.objects.get(pk=storage_id)
        serialized_clients = StorageReadSerializer(data=storage.__dict__)

        if serialized_clients.is_valid():
            return Response(serialized_clients.data, status=status.HTTP_200_OK)

        return Response(serialized_clients.errors, status=status.HTTP_400_BAD_REQUEST)
    except ObjectDoesNotExist:
        return Response({"Error": f"Storage not found"}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"Error": f"Unexpected error {e} occurred."}, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(method='GET', tags=["Storage"])
@api_view(['GET'])
def read_storages(request: Request
                  ) -> Response:
    storages = Storage.objects.all()

    serialized_clients = StorageReadSerializer(data=list(storages.values()), many=True)

    if serialized_clients.is_valid():
        return Response(serialized_clients.data, status=status.HTTP_200_OK)

    return Response(serialized_clients.errors, status=status.HTTP_400_BAD_REQUEST)
