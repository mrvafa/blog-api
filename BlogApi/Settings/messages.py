from django.conf import settings

ERROR_MESSAGES = {
    'AGE_MIN': f'Your age should be at last {settings.AGE_MIN}',
    'AGE_MAX': f'Your age should be at most {settings.AGE_MAX}',
    'WRONG_IRN_PHONE_NUMBER': 'Please input correct iran phone number format',
    'PROFILE_IMAGE_ALLOWED_EXTENSIONS':
        f'Please select an image format (valid formats are {settings.PROFILE_IMAGE_ALLOWED_EXTENSIONS}).',
    'PROFILE_IMAGE_WIDTH_MAX': f'Max profile image width length is {settings.PROFILE_IMAGE_WIDTH_MAX}',
    'PROFILE_IMAGE_HEIGHT_MAX': f'Max profile image height is {settings.PROFILE_IMAGE_HEIGHT_MAX}',
    'PROFILE_IMAGE_SIZE_MAX': f'Max profile image size length is {settings.PROFILE_IMAGE_SIZE_MAX}',
    'PROFILE_IMAGE_WIDTH_MIN': f'Min profile image width length is {settings.PROFILE_IMAGE_WIDTH_MIN}',
    'PROFILE_IMAGE_HEIGHT_MIN': f'Min profile image height is {settings.PROFILE_IMAGE_HEIGHT_MIN}',

    'TAG_IMAGE_ALLOWED_EXTENSIONS':
        f'Please select an image format (valid formats are {settings.TAG_IMAGE_ALLOWED_EXTENSIONS}).',
    'TAG_IMAGE_WIDTH_MAX': f'Max tag image width length is {settings.TAG_IMAGE_WIDTH_MAX}',
    'TAG_IMAGE_HEIGHT_MAX': f'Max tag image height is {settings.TAG_IMAGE_HEIGHT_MAX}',
    'TAG_IMAGE_SIZE_MAX': f'Max tag image size length is {settings.TAG_IMAGE_SIZE_MAX}',
    'TAG_IMAGE_WIDTH_MIN': f'Min tag image width length is {settings.TAG_IMAGE_WIDTH_MIN}',
    'TAG_IMAGE_HEIGHT_MIN': f'Min tag image height is {settings.TAG_IMAGE_HEIGHT_MIN}',

    'POST_IMAGE_FORMAT_INVALID':
        f'Please select an image format (valid formats are {settings.POST_ALLOWED_IMAGE_EXTENSIONS}).',
    'POST_IMAGE_WIDTH_MAX': f'Max post image width length is {settings.POST_IMAGE_WIDTH_MAX}',
    'POST_IMAGE_HEIGHT_MAX': f'Max post image height is {settings.POST_IMAGE_HEIGHT_MAX}',
    'POST_IMAGE_SIZE_MAX': f'Max post image size length is {settings.POST_IMAGE_SIZE_MAX}',
    'POST_IMAGE_WIDTH_MIN': f'Min post image width length is {settings.POST_IMAGE_WIDTH_MIN}',
    'POST_IMAGE_HEIGHT_MIN': f'Min post image height is {settings.POST_IMAGE_HEIGHT_MIN}',
}
