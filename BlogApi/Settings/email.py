import os

from dotenv import load_dotenv

load_dotenv()

EMAIL_BACKEND = os.getenv('EMAIL_BACKEND')
EMAIL_HOST = os.getenv('EMAIL_HOST')
EMAIL_PORT = os.getenv('EMAIL_PORT')
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
EMAIL_USE_SSL = os.getenv('EMAIL_USE_SSL')
EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS')

EMAIL_VALIDATION = os.getenv('EMAIL_VALIDATION')
