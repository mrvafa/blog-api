import PIL.Image
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import InMemoryUploadedFile
from filetype import filetype


def post_image_validate(image):
    if type(image) is InMemoryUploadedFile:
        return
    kind = filetype.guess(image)
    if not kind or kind.extension not in settings.POST_ALLOWED_IMAGE_EXTENSIONS:
        raise ValidationError(
            settings.ERROR_MESSAGES['POST_IMAGE_FORMAT_INVALID']
        )

    im = PIL.Image.open(image)
    width, height = im.size

    errors = []

    if width > settings.POST_IMAGE_WIDTH_MAX:
        errors.append(
            settings.ERROR_MESSAGES['POST_IMAGE_WIDTH_MAX']
        )

    elif width < settings.POST_IMAGE_WIDTH_MIN:
        errors.append(
            settings.ERROR_MESSAGES['POST_IMAGE_WIDTH_MIN']
        )

    if height > settings.POST_IMAGE_HEIGHT_MAX:
        errors.append(
            settings.ERROR_MESSAGES['POST_IMAGE_HEIGHT_MAX']
        )

    if height < settings.POST_IMAGE_HEIGHT_MIN:
        errors.append(
            settings.ERROR_MESSAGES['POST_IMAGE_HEIGHT_MIN']
        )

    if image.size / (1024 ** 2) > settings.POST_IMAGE_SIZE_MAX:
        errors.append(
            settings.ERROR_MESSAGES['POST_IMAGE_SIZE_MAX']
        )

    if errors:
        raise ValidationError(errors)
