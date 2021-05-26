from datetime import datetime

from django.conf import settings
from django.core.exceptions import ValidationError
from django.test import TestCase

from Validators.birthday_validators import age_min_validator, age_max_validator


class TestBirthdayValidator(TestCase):
    def test_ok_age_min_validator(self):
        res = age_min_validator(datetime(datetime.now().year - settings.AGE_MIN - 1, 10, 11))
        self.assertIsNone(res)

    def test_wrong_age_min_validator(self):
        with self.assertRaises(ValidationError):
            age_min_validator(datetime(datetime.now().year, 10, 11))

    def test_ok_age_min_edge_validator(self):
        res = age_min_validator(datetime(datetime.now().year - settings.AGE_MIN,
                                         datetime.now().month, datetime.now().day))
        self.assertIsNone(res)

    def test_wrong_age_min_edge_validator(self):
        with self.assertRaises(ValidationError):
            age_min_validator(
                datetime(datetime.now().year - settings.AGE_MIN, datetime.now().month, datetime.now().day + 1))

    def test_ok_age_max_validator(self):
        res = age_max_validator(datetime(datetime.now().year - settings.AGE_MAX + 1, 10, 11))
        self.assertIsNone(res)

    def test_wrong_age_max_validator(self):
        with self.assertRaises(ValidationError):
            age_max_validator(datetime(datetime.now().year - settings.AGE_MAX - 2, 10, 11))

    def test_ok_age_max_edge_validator(self):
        res = age_max_validator(datetime(datetime.now().year - settings.AGE_MAX,
                                         datetime.now().month, datetime.now().day + 1))
        self.assertIsNone(res)

    def test_wrong_age_max_edge_validator(self):
        with self.assertRaises(ValidationError):
            age_max_validator(datetime(datetime.now().year - settings.AGE_MAX - 1,
                                       datetime.now().month, datetime.now().day - 1))
