from io import BytesIO

from django.core.files.uploadedfile import InMemoryUploadedFile
from rest_framework import serializers
from .models import User
from django.contrib.auth.password_validation import validate_password
from PIL import Image, ImageEnhance
from django.core.files import File

BASIC_AVATAR = 'media/basic_avatar.jpeg'
WATERMARK = 'main/static/main/img/water.png'


def generate_avatar_with_watermark(avatar):
    original_file = avatar

    image = Image.open(avatar)
    watermark = Image.open(WATERMARK)
    image_with_watermark = add_watermark(image, watermark)

    buffer = BytesIO()
    format_ = original_file.content_type.split('/')[-1]
    image_with_watermark.save(buffer, format_)
    converted_file = InMemoryUploadedFile(
        buffer,
        original_file.field_name,
        original_file.name,
        original_file.content_type,
        buffer.tell(),
        None
    )

    return converted_file


def add_watermark(image, watermark, opacity=1):
    assert 0 <= opacity <= 1
    if opacity < 1:
        if watermark.mode != 'RGBA':
            watermark = watermark.convert('RGBA')
        else:
            watermark = watermark.copy()
        alpha = watermark.split()[3]
        alpha = ImageEnhance.Brightness(alpha).enhance(opacity)
        watermark.putalpha(alpha)
    layer = Image.new('RGBA', image.size, (0, 0, 0, 0))
    layer.paste(watermark, (1, 1))
    return Image.composite(layer, image, layer)


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
        else:
            validated_data['avatar'] = generate_avatar_with_watermark(validated_data['avatar'])

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
