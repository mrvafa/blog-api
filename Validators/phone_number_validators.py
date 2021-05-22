from django.core.exceptions import ValidationError

from BlogApi.Settings.messages import ERROR_MESSAGES
from Validators.collectins import pattern_validation


def iran_phone_validate(value):
    errors = []
    if value:
        if not pattern_validation(value, r'(\+98|0)?9\d{9}'):
            errors.append(ERROR_MESSAGES['WRONG_IRN_PHONE_NUMBER'])

    if errors:
        raise ValidationError(errors)
