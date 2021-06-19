import phonenumbers
from django.core.exceptions import ValidationError

from BlogApi.Settings.messages import ERROR_MESSAGES


def iran_phone_validate(value):
    errors = []
    if value:
        if not value.startswith('0') and not value.startswith('+98'):
            errors.append(ERROR_MESSAGES['WRONG_IRAN_PHONE_NUMBER'])
        elif not phonenumbers.is_valid_number(phonenumbers.parse(value, "IR")):
            errors.append(ERROR_MESSAGES['WRONG_IRAN_PHONE_NUMBER'])
    if errors:
        raise ValidationError(errors)
