from rest_framework import serializers
from account.models import User


class VerifySerializer(serializers.Serializer):
    phone = serializers.CharField()
    password = serializers.CharField()


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "phone",
            "user_name",
            "postal_code",
            "location",
            "address",
            "city",
            "avatar",
        )
        read_only_fields = ("phone",)


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("user_name", "phone")


class LoginSerializer(serializers.Serializer):
    phone = serializers.CharField()


class GeneralSerializer(serializers.Serializer):
    message = serializers.CharField()


class TokenSerializer(serializers.Serializer):
    refresh = serializers.CharField()
    access = serializers.CharField()


# user for update user
class UpdateProfileSerializer(serializers.Serializer):
    class Meta:
        model = User

    fields = (
        "email",
        "country",
        "city",
        "city_location",
        "address",
        "postal_code",
        "password",
        "location",
        "avatar",
    )
