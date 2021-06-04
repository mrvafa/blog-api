from django.contrib.auth.models import Permission
from django.core.exceptions import ValidationError
from rest_framework import serializers
from rest_framework.authtoken.models import Token

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
    is_author = serializers.BooleanField()

    class Meta:
        model = User
        fields = ('is_author',)

    def update(self, *args, **kwargs):
        user = args[0]
        is_author = args[1]['is_author']
        permission = Permission.objects.get(codename='is_author')
        if is_author:
            user.user_permissions.add(permission)
        else:
            user.user_permissions.remove(permission)
        return super(AuthorUserSerializers, self).update(*args, **kwargs)


class EditUserStatusSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('is_active', 'is_staff', 'is_superuser')


class UserChangePasswordSerializer(serializers.ModelSerializer):
    new_password1 = serializers.CharField(
        write_only=True,
        required=True,
    )

    new_password2 = serializers.CharField(
        write_only=True,
        required=True,
    )

    def validate(self, data):
        return super(UserChangePasswordSerializer, self).validate(data)

    def update(self, *args, **kwargs):
        user = args[0]
        new_password1 = args[1]['new_password1']
        new_password2 = args[1]['new_password2']
        if new_password1 == new_password2:
            if user.check_password(new_password1):
                raise serializers.ValidationError({'error': 'Please enter new password.'})
            try:
                user.set_password(new_password1)
                user.save()
                Token.objects.get(user=user).delete()
                Token.objects.create(user=user)
            except ValidationError as e:
                raise serializers.ValidationError({'errors': e.messages})
        else:
            raise serializers.ValidationError({'error': 'Password does not mach'})

        return super(UserChangePasswordSerializer, self).update(*args, **kwargs)

    class Meta:
        model = User
        fields = ('new_password1', 'new_password2')
