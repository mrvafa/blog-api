import os

import requests
from django.conf import settings
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db import models

from Profile.validators.birthday_validators import age_max_validator, age_min_validator
from Profile.validators.phone_number_validators import iran_phone_validate
from Profile.validators.profile_image_validator import profile_image_validate


class Position(models.Model):
    position = models.CharField(max_length=100, unique=True, primary_key=True, )

    def __str__(self):
        return self.position

    @staticmethod
    def create_positions():
        for position in settings.POSITION_CHOICES:
            if not Position.objects.filter(position=position):
                Position.objects.create(position=position).save()


class Profile(models.Model):
    # django user model has first_name, last_name, email, joined_time and password
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
        unique=True
    )
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
    phone_number = models.TextField(
        blank=True,
        null=True,
        max_length=settings.PHONE_NUMBER_MAX_LENGTH,
        validators=[iran_phone_validate],
        unique=True,
    )
    phone_number_verified = models.BooleanField(default=False)
    # TODO: notifications using message model
    image = models.ImageField(
        blank=True,
        null=True,
        upload_to='profile_images/%m',
        validators=[profile_image_validate]
    )

    positions = models.ManyToManyField(
        Position,
        blank=True,
    )

    def get_positions(self):
        return " ".join([str(pos) for pos in self.positions.all()])

    def __str__(self):
        return self.user.username

    def clean(self, *args, **kwargs):
        if self.phone_number and self.phone_number.startswith('0'):
            self.phone_number = '+98' + self.phone_number[1:]
        if 'admin' in self.get_positions().split(' '):
            self.user.is_staff = True
            self.user.save()
        if 'superuser' in self.get_positions().split(' '):
            self.user.is_superuser = True
            self.user.is_staff = True
            self.user.save()
        if not self.phone_number:
            self.phone_number = None
        super(Profile, self).clean()

    def save(self, *args, **kwargs):
        self.full_clean()
        super(Profile, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.image:
            os.remove(self.image.path)
        super(Profile, self).delete(*args, **kwargs)

    def set_profile_image(self, image_path):
        image_content = requests.get(image_path).content \
            if image_path.startswith('http://') or image_path.startswith('https://') else open(image_path, 'rb').read()
        image_name = os.path.basename(image_path)
        old_image_path = ''
        if self.image and os.path.isfile(self.image.path):
            old_image_path = self.image.path
        self.image = SimpleUploadedFile(
            name=image_name,
            content_type='image/jpeg',
            content=image_content,
        )
        self.save()

        if old_image_path:
            os.remove(old_image_path)
