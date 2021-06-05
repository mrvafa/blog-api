from PIL import Image
from django.conf import settings
from django.core.exceptions import ValidationError


def _is_allowed_extension(image, valid_extensions):
    img = Image.open(image)
    if img.format.lower() not in valid_extensions:
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


def _check_min_max_width_length_size_image_extensions(
        image,
        width_max,
        height_max,
        width_min,
        height_min,
        size_max,
        allowed_extensions,
):
    errors = {
        'width_max': False,
        'height_max': False,
        'width_min': False,
        'height_min': False,
        'size_max': False,
        'image_extensions': False,
        'size_min': False,
    }
    if not _is_allowed_extension(image, allowed_extensions):
        errors['allowed_extensions'] = True
        return errors

    im = Image.open(image)
    if not _is_image_width_less_than_or_equal(im, width_max):
        errors['width_max'] = True

    elif not _is_image_width_more_than_or_equal(im, width_min):
        errors['width_min'] = True

    if not _is_image_height_less_than_or_equal(im, height_max):
        errors['height_max'] = True

    elif not _is_image_height_more_than_or_equal(im, height_min):
        errors['height_min'] = True

    if not _is_image_size_is_less_than_or_equal(image, size_max):
        errors['size_max'] = True

    return errors


def profile_image_validate(image):
    errors = _check_min_max_width_length_size_image_extensions(
        image=image,
        allowed_extensions=settings.PROFILE_IMAGE_ALLOWED_EXTENSIONS,
        width_max=settings.PROFILE_IMAGE_WIDTH_MAX,
        width_min=settings.PROFILE_IMAGE_WIDTH_MIN,
        height_max=settings.PROFILE_IMAGE_HEIGHT_MAX,
        height_min=settings.PROFILE_IMAGE_HEIGHT_MIN,
        size_max=settings.PROFILE_IMAGE_SIZE_MAX,
    )
    error_messages = []
    for key in errors:
        if errors[key]:
            error_messages.append(settings.ERROR_MESSAGES[f'PROFILE_IMAGE_{key.upper()}'])

    if error_messages:
        raise ValidationError(error_messages)


def tag_image_validate(image):
    errors = _check_min_max_width_length_size_image_extensions(
        image=image,
        allowed_extensions=settings.TAG_IMAGE_ALLOWED_EXTENSIONS,
        width_max=settings.TAG_IMAGE_WIDTH_MAX,
        width_min=settings.TAG_IMAGE_WIDTH_MIN,
        height_max=settings.TAG_IMAGE_HEIGHT_MAX,
        height_min=settings.TAG_IMAGE_HEIGHT_MIN,
        size_max=settings.TAG_IMAGE_SIZE_MAX,
    )
    error_messages = []
    for key in errors:
        if errors[key]:
            error_messages.append(settings.ERROR_MESSAGES[f'TAG_IMAGE_{key.upper()}'])

    if error_messages:
        raise ValidationError(error_messages)
