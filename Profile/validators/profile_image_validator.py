import filetype
from PIL import Image
from django.core.exceptions import ValidationError
from django.conf import settings


def profile_image_validate(image):
    kind = filetype.guess(image)
    if not kind.extension and kind.extension not in settings.PROFILE_ALLOWED_IMAGE_EXTENSIONS:
        raise ValidationError(
            settings.ERROR_MESSAGES['PROFILE_IMAGE_FORMAT_INVALID']
        )

    im = Image.open(image)
    width, height = im.size

    errors = []

    if width > settings.PROFILE_IMAGE_WIDTH_MAX:
        errors.append(
            settings.ERROR_MESSAGES['PROFILE_IMAGE_WIDTH_MAX']
        )

    elif width < settings.PROFILE_IMAGE_WIDTH_MIN:
        errors.append(
            settings.ERROR_MESSAGES['PROFILE_IMAGE_WIDTH_MIN']
        )

    if height > settings.PROFILE_IMAGE_HEIGHT_MAX:
        errors.append(
            settings.ERROR_MESSAGES['PROFILE_IMAGE_HEIGHT_MAX']
        )

    if height < settings.PROFILE_IMAGE_HEIGHT_MIN:
        errors.append(
            settings.ERROR_MESSAGES['PROFILE_IMAGE_HEIGHT_MIN']
        )

    if image.size / (1024 ** 2) > settings.PROFILE_IMAGE_SIZE_MAX:
        errors.append(
            settings.ERROR_MESSAGES['PROFILE_IMAGE_SIZE_MAX']
        )

    if errors:
        raise ValidationError(errors)
