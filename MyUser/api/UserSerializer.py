from rest_framework import serializers

from MyUser.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ('password',)


class EditUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'gender', 'birthday', 'phone_number', 'image',)


class AuthorUserSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('is_author',)


class EditUserStatusSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('is_active', 'is_staff', 'is_superuser')
