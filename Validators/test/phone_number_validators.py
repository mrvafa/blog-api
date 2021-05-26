from django.core.exceptions import ValidationError
from django.test import TestCase

from Validators.phone_number_validators import iran_phone_validate


class TestPhoneNumberValidators(TestCase):
    def test_ok_iran_phone_validate_starts_with_09(self):
        res = iran_phone_validate('09131234567')
        self.assertIsNone(res)

    def test_ok_iran_phone_validate_starts_with_plus98(self):
        res = iran_phone_validate('09131234567')
        self.assertIsNone(res)

    def test_wrong_iran_phone_validate_less_number_09(self):
        with self.assertRaises(ValidationError):
            iran_phone_validate('0913123456')

    def test_wrong_iran_phone_validate_less_number_plus98(self):
        with self.assertRaises(ValidationError):
            iran_phone_validate('+9831234567')
