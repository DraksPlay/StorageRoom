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
    CategoryReadSerializer
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
        storage = Storage.objects.filter(pk=storage_id)
        storage_serializer = StorageReadSerializer(data=storage.values())

        if storage_serializer.is_valid():
            return Response(storage_serializer.data, status=status.HTTP_200_OK)

        return Response(storage_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except ObjectDoesNotExist:
        return Response({"Error": f"Storage not found"}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"Error": f"Unexpected error {e} occurred."}, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(method='GET', tags=["Storage"])
@api_view(['GET'])
def read_storages(request: Request
                  ) -> Response:
    storages = Storage.objects.all()

    storages_list = list(storages.values(
        "id", "category__name", "user__email", "price", "start_at", "finish_at"
    ))

    storage_serializer = StorageReadSerializer(data=storages_list, many=True)

    if storage_serializer.is_valid():
        return Response(storage_serializer.data, status=status.HTTP_200_OK)

    return Response(storage_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(method='GET', tags=["Category"])
@api_view(['GET'])
def read_categories(request: Request
                    ) -> Response:
    categories = Category.objects.all()

    category_serializer = CategoryReadSerializer(data=list(categories.values()), many=True)

    if category_serializer.is_valid():
        return Response(category_serializer.data, status=status.HTTP_200_OK)

    return Response(category_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
