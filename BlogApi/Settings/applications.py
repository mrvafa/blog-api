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
    'django_cleanup',

    'rest_auth.registration',

    'django_rest_allauth',
    'rest_framework',
    'rest_framework.authtoken',

    'ckeditor',
    'ckeditor_uploader',

    'Tag.apps.TagConfig',
    'Post.apps.PostConfig',
    'MyUser.apps.MyuserConfig',
]
