from rest_framework import serializers

from applications.users.models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = "__all__"


class UserUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = "__all__"

    def update(self,
               instance: User,
               validated_data: dict
               ) -> User:
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()

        return instance
