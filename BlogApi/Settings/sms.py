# expire duration in minute
import os

from dotenv import load_dotenv

EXPIRE_DURATION = 5

# max fail code entering
SMS_MAX_TRY_CODE = 5

SMS_BACKEND = 'sms.backends.console.SmsBackend'

load_dotenv()
# SMS_BACKEND = 'sms.backends.kavenegar.SmsBackend'
KAVENEGAR_API_KEY = os.getenv('KAVENEGAR_API_KEY')
KAVENEGAR_SENDER = os.getenv('KAVENEGAR_SENDER')

# Don't change the value
SMS_CODE_FOR_TEST = ''
