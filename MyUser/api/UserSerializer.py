from django.contrib.auth.models import Permission
from django.core.exceptions import ValidationError
from rest_framework import serializers
from rest_framework.authtoken.models import Token

from MyUser.models import User, SMSCode


class PrivateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ('password',)
        read_only_fields = ('phone_number',)


class PublicAuthorsSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('gender', 'birthday', 'image', 'username',)


class PublicUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('gender', 'birthday', 'image', 'username', 'posts')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ('password',)
        read_only_fields = ('phone_number',)


class EditUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'gender', 'birthday', 'image', 'phone_number')
        read_only_fields = ('phone_number',)


class AuthorUserSerializers(serializers.ModelSerializer):
    is_author = serializers.BooleanField()

    class Meta:
        model = User
        fields = ('is_author',)

    def update(self, *args, **kwargs):
        user = args[0]
        if 'is_author' not in args[1]:
            return super(AuthorUserSerializers, self).update(*args, **kwargs)
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
        new_password1 = args[1]['new_password1'] if 'new_password1' in args[1] else None
        new_password2 = args[1]['new_password2'] if 'new_password2' in args[1] else None
        if not new_password1 or not new_password2:
            raise serializers.ValidationError({'errors': 'new_password1 and new_password2 is required.'})
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


class SetPhoneNumberSerializer(serializers.ModelSerializer):
    code = serializers.CharField(required=True, write_only=True, )
    phone_number = serializers.CharField(required=True, )

    class Meta:
        model = User
        fields = ('phone_number', 'code')

    def update(self, instance, validated_data):
        if 'phone_number' not in validated_data or 'code' not in validated_data:
            raise serializers.ValidationError({'error': 'code and phone_number is required'})

        phone_number = validated_data['phone_number'] if validated_data['phone_number'].startswith('+98') else \
            '+98' + validated_data['phone_number'][1:]
        user_code = validated_data['code']

        try:
            code = SMSCode.get_code_for_phone_number(phone_number)
        except Exception as e:
            raise serializers.ValidationError({'errors': e.messages})

        if user_code == code:
            try:
                instance.set_phone_number(new_phone_number=phone_number)
            except Exception as e:
                raise serializers.ValidationError({'error': e.messages})
            return instance
        else:
            raise serializers.ValidationError({'error': 'Code is wrong.'})


class GenerateSMSCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SMSCode
        fields = ('phone_number', 'created_datetime', 'expired_datetime',)
        read_only_fields = ('created_datetime', 'expired_datetime')

    def create(self, validated_data):
        if 'phone_number' not in validated_data:
            raise serializers.ValidationError('phone_number if required.')

        phone_number = validated_data['phone_number'] if validated_data['phone_number'].startswith('+98') else \
            '+98' + validated_data['phone_number'][1:]

        if User.objects.filter(phone_number=phone_number).first():
            raise serializers.ValidationError('Account with this phone number exist.')

        try:
            SMSCode.send_sms(phone_number=phone_number)
        except Exception as e:
            raise serializers.ValidationError({'errors': e.messages})

        sms_object = SMSCode.objects.filter(phone_number=phone_number).first()
        return sms_object
