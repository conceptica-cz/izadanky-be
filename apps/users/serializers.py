from rest_framework import serializers

from .models import User


class UserLightSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = read_only_fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
        )


class UserSerializer(serializers.ModelSerializer):
    person = serializers.PrimaryKeyRelatedField(source="get_person", read_only=True)

    class Meta:
        model = User

        fields = read_only_fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "person",
        )
