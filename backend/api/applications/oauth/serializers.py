from rest_framework import serializers

from applications.oauth.models import Token


class TokenSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()


class TokenUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Token
        fields = "__all__"

    def update(self,
               instance: Token,
               validated_data: dict
               ) -> Token:
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()

        return instance
