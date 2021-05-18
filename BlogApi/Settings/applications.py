# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    'allauth',
    'allauth.account',
    'allauth.socialaccount',

    'rest_auth.registration',

    'django_rest_allauth',
    'rest_framework',
    'rest_framework.authtoken',

    'ckeditor',
    'ckeditor_uploader',

    'Profile.apps.ProfileConfig',
    'Tag.apps.TagConfig',
    'Post.apps.PostConfig',
]
