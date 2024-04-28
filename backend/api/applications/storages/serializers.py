from rest_framework import serializers

from applications.storages.models import (
    Storage,
    Category
)


class StorageSerializer(serializers.Serializer):
    category_id = serializers.IntegerField()
    user_id = serializers.IntegerField()
    price = serializers.DecimalField(max_digits=12, decimal_places=2)
    start_at = serializers.DateTimeField()
    finish_at = serializers.DateTimeField()


class StorageReadSerializer(serializers.ModelSerializer):

    class Meta:
        model = Storage
        fields = "__all__"


class CategoryReadSerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = "__all__"
