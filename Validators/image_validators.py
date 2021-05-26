import filetype
from PIL import Image
from django.core.exceptions import ValidationError
from django.conf import settings
from django.core.files.uploadedfile import InMemoryUploadedFile


def _is_allowed_extension(image, valid_extensions):
    kind = filetype.guess(image)
    if not kind or kind.extension not in valid_extensions:
        return False
    return True


def _is_image_width_less_than_or_equal(im, width):
    image_width, _ = im.size
    return image_width <= width


def _is_image_width_more_than_or_equal(im, width):
    image_width, _ = im.size
    return image_width >= width


def _is_image_height_less_than_or_equal(im, height):
    _, image_height = im.size
    return image_height <= height


def _is_image_height_more_than_or_equal(im, height):
    _, image_height = im.size
    return image_height >= height


def _is_image_size_is_less_than_or_equal(image, size_in_megabyte):
    return image.size / (1024 ** 2) <= size_in_megabyte


def profile_image_validate(image):
    # if type(image) is not InMemoryUploadedFile:
    #     return
    if not _is_allowed_extension(image, settings.PROFILE_ALLOWED_IMAGE_EXTENSIONS):
        raise ValidationError(
            settings.ERROR_MESSAGES['PROFILE_IMAGE_FORMAT_INVALID']
        )

    errors = []

    im = Image.open(image)

    if not _is_image_width_less_than_or_equal(im, settings.PROFILE_IMAGE_WIDTH_MAX):
        errors.append(
            settings.ERROR_MESSAGES['PROFILE_IMAGE_WIDTH_MAX']
        )

    elif not _is_image_width_more_than_or_equal(im, settings.PROFILE_IMAGE_WIDTH_MIN):
        errors.append(
            settings.ERROR_MESSAGES['PROFILE_IMAGE_WIDTH_MIN']
        )

    if not _is_image_height_less_than_or_equal(im, settings.PROFILE_IMAGE_HEIGHT_MAX):
        errors.append(
            settings.ERROR_MESSAGES['PROFILE_IMAGE_HEIGHT_MAX']
        )

    elif not _is_image_height_more_than_or_equal(im, settings.PROFILE_IMAGE_HEIGHT_MIN):
        errors.append(
            settings.ERROR_MESSAGES['PROFILE_IMAGE_HEIGHT_MIN']
        )

    if not _is_image_size_is_less_than_or_equal(image, settings.PROFILE_IMAGE_SIZE_MAX):
        errors.append(
            settings.ERROR_MESSAGES['PROFILE_IMAGE_SIZE_MAX']
        )

    if errors:
        raise ValidationError(errors)
