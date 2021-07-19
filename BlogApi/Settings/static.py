# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/
import os

from django.conf import settings

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(os.path.dirname(settings.BASE_DIR), 'static')
