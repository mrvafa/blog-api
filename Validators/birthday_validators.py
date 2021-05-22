from datetime import datetime

from dateutil.relativedelta import relativedelta
from django.core.exceptions import ValidationError

from BlogApi.Settings.fields import AGE_MIN, AGE_MAX
from BlogApi.Settings.messages import ERROR_MESSAGES


def age_min_validator(value):
    errors = []
    if relativedelta(datetime.now(), value).years < AGE_MIN:
        errors.append(ERROR_MESSAGES['AGE_MIN'])
    if errors:
        raise ValidationError(
            errors
        )


def age_max_validator(value):
    errors = []
    if relativedelta(datetime.now(), value).years > AGE_MAX:
        errors.append(ERROR_MESSAGES['AGE_MAX'])

    if errors:
        raise ValidationError(
            errors
        )
