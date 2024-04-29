from rest_framework import serializers

from applications.users.models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = "__all__"


class UserReadSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "balance"
        )


class UserUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            "email",
            "password",
            "balance"
        )

    def update(self,
               instance: User,
               validated_data: dict
               ) -> User:
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()

        return instance
