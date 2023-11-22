from django.contrib.auth import get_user_model
from rest_framework import serializers

from .helpers import check_password_strength

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, min_length=8)
    name = serializers.CharField(min_length=5, max_length=255)
    username = serializers.CharField(min_length=8, max_length=100)
    password = serializers.CharField(min_length=10, write_only=True)
    password_confirmation = serializers.CharField(min_length=10, write_only=True)

    class Meta:
        model = User
        fields = ["name", "username", "email", "password", "password_confirmation"]

    def validate(self, attrs):
        if not attrs.get("name"):
            raise serializers.ValidationError({"name_error": "You didnt insert a name"})
        if not attrs.get("username"):
            raise serializers.ValidationError(
                {"username_error": "You didn't insert a username"}
            )
        if not attrs.get("email"):
            raise serializers.ValidationError(
                {"email_error", "You didn't insert a email"}
            )
        if not attrs.get("password"):
            raise serializers.ValidationError(
                {"password_error", "You didn't insert a Password"}
            )
        if not attrs.get("password_confirmation"):
            raise serializers.ValidationError(
                {
                    "password_confirmation_error",
                    "You didn't insert The Password Confimation",
                }
            )
        if attrs.get("password") != attrs.get("password_confirmation"):
            raise serializers.ValidationError(
                {
                    "password_confirmation_error": "Password and Password Confimation are not identical"
                }
            )

        if not check_password_strength(attrs.get("password")):
            raise serializers.ValidationError(
                {
                    "password_strength_error": "Password should contain at lowercase/uppercase characters and numbers"
                }
            )
        if User.objects.filter(email=attrs["email"].lower()):
            raise serializers.ValidationError(
                {"email_duplication": "This email already exists"}
            )
        if User.objects.filter(username=attrs["username"]):
            raise serializers.ValidationError(
                {"username_duplication": "This username already exists"}
            )
        return attrs

    def create(self, validation_data):
        return User.objects.create_user(
            name=validation_data["name"],
            email=validation_data["email"].lower(),
            username=validation_data["username"],
            password=validation_data["password"],
        )