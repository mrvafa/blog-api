from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.password_validation import validate_password
from django.db import models
from django.utils.translation import gettext_lazy as _

from Validators.birthday_validators import age_min_validator, age_max_validator
from Validators.image_validators import profile_image_validate
from Validators.phone_number_validators import iran_phone_validate


class User(AbstractUser):
    email = models.EmailField(_('email address'), blank=True, unique=True)
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
    phone_number_verified = models.BooleanField(default=False, editable=False)

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
        if not self.email:
            self.email = None
        super(User, self).clean()

    def save(self, *args, **kwargs):
        self.full_clean(exclude=('password',))
        super(User, self).save(*args, **kwargs)

    def is_author(self):
        return self.has_perm('Post.is_author')

    def set_phone_number(self, new_phone_number):
        self.phone_number_verified = False
        self.phone_number = new_phone_number
        self.save()

    def __str__(self):
        return self.username
