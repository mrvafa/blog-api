import datetime
import random

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from Validators.birthday_validators import age_min_validator, age_max_validator
from Validators.image_validators import profile_image_validate
from Validators.phone_number_validators import iran_phone_validate
from kavenegar.kavenegar import KavenegarAPI


class User(AbstractUser):
    email = models.EmailField(_('email address'), blank=True, unique=False)
    gender = models.TextField(
        blank=True,
        null=True,
        choices=settings.GENDER_CHOICES,
        max_length=max(len(p[0]) for p in settings.GENDER_CHOICES)
    )
    birthday = models.DateField(
        blank=True,
        null=True,
        validators=[age_min_validator, age_max_validator]
    )
    phone_number = models.CharField(
        blank=True,
        null=True,
        max_length=settings.PHONE_NUMBER_MAX_LENGTH,
        validators=[iran_phone_validate],
        unique=True,
    )

    image = models.ImageField(
        blank=True,
        null=True,
        upload_to='profile_images/%m',
        validators=[profile_image_validate]
    )

    def set_password(self, raw_password):
        validate_password(raw_password)
        return super(User, self).set_password(raw_password)

    def clean(self, *args, **kwargs):
        if not self.phone_number:
            self.phone_number = None
        user_with_this_email = User.objects.filter(email=self.email).first()
        if self.email and user_with_this_email and not user_with_this_email == self:
            raise ValidationError('Email has taken')
        super(User, self).clean()

    def save(self, *args, **kwargs):
        self.full_clean(exclude=('password',))
        super(User, self).save(*args, **kwargs)

    def is_author(self):
        return self.has_perm('Post.is_author')

    def set_phone_number(self, new_phone_number):
        if new_phone_number[0] == '0':
            new_phone_number = '+98' + new_phone_number[1:]
        self.phone_number = new_phone_number
        self.save()

    def set_user_to_author(self):
        author_permission = Permission.objects.get(codename='is_author')
        self.user_permissions.add(author_permission)
        self.save()

    def __str__(self):
        return self.username


class SMSCode(models.Model):
    phone_number = models.CharField(
        max_length=settings.PHONE_NUMBER_MAX_LENGTH,
        validators=[iran_phone_validate],
        unique=True,
    )
    created_datetime = models.DateTimeField(auto_now_add=True, blank=True, null=True, )
    expired_datetime = models.DateTimeField(
        default=timezone.now() + datetime.timedelta(minutes=settings.EXPIRE_DURATION),
        blank=True,
        null=True,
    )
    code = models.CharField(max_length=100)
    tried = models.PositiveSmallIntegerField(default=0)

    @staticmethod
    def send_sms(phone_number):
        sms_code = SMSCode.objects.filter(phone_number=phone_number).first()

        if sms_code:
            if sms_code.expired_datetime > timezone.now():
                raise ValidationError('Previous code is not expired yet.')
            else:
                sms_code.delete()

        code = random.randint(10000000, 99999999) if not settings.SMS_CODE_FOR_TEST else settings.SMS_CODE_FOR_TEST

        respond = _send_sms(phone_number, text=code)
        SMSCode.objects.create(phone_number=phone_number, code=code)
        return code, respond

    @staticmethod
    def get_code_for_phone_number(phone_number):
        sms_code = SMSCode.objects.filter(phone_number=phone_number).first()
        if not sms_code:
            raise ValidationError('Phone number not found.')
        if timezone.now() > sms_code.expired_datetime:
            sms_code.delete()
            raise ValidationError('Code expired.')

        sms_code.tried += 1
        sms_code.save()

        if sms_code.tried > settings.SMS_MAX_TRY_CODE:
            raise ValidationError('Too many requests.')

        return sms_code.code

    def clean(self, *args, **kwargs):
        if self.phone_number[0] == '0':
            self.phone_number = '+98' + self.phone_number[1:]
        super(SMSCode, self).clean()

    def save(self, *args, **kwargs):
        self.full_clean()
        super(SMSCode, self).save(*args, **kwargs)


def _send_sms(phone_number, text):
    if settings.SMS_BACKEND == 'sms.backends.console.SmsBackend':
        print('Sender', 'Django Backend SMS')
        print('Receiver', phone_number)
        print(text)
        print("".join(['-' for _ in range(20)]))
    elif settings.SMS_BACKEND == 'sms.backends.kavenegar.SmsBackend':
        api = KavenegarAPI(settings.KAVENEGAR_API_KEY)
        params = {'sender': settings.KAVENEGAR_SENDER, 'receptor': phone_number, 'message': text}
        response = api.sms_send(params)
        return response
