from rest_framework import serializers
from .models import User
from django.contrib.auth.password_validation import validate_password
from django.core.files import File

BASIC_AVATAR = 'media/basic_avatar.jpeg'


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'gender',
            'email',
            'avatar',
            'password',
            'password2',
        ]

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user_didnt_send_avatar = 'avatar' not in validated_data
        if user_didnt_send_avatar:
            file = open(BASIC_AVATAR, 'rb')
            validated_data['avatar'] = File(file)

        user = User.objects.create(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            avatar=validated_data['avatar'],
        )

        if user_didnt_send_avatar:
            file.close()

        user.set_password(validated_data['password'])
        user.save()
        return user
