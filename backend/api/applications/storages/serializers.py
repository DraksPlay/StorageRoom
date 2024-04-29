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
    category__name = serializers.CharField(max_length=255)
    user__email = serializers.CharField(max_length=255)

    class Meta:
        model = Storage
        fields = ['category__name', 'user__email', 'price', 'start_at', 'finish_at']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['category'] = data.pop('category__name')
        data['user'] = data.pop('user__email')

        return data

class CategoryReadSerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = "__all__"
