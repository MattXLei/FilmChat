from pathlib import Path
from decouple import config

DEBUG = config('DEBUG', default=False, cast=bool)

ALLOWED_HOSTS = ["www.moviechat-club.chat", 18.118.25.84, 172.31.41.234, 127.0.0.1]

ROOT_URLCONF = f'{config("ChatServerPlayground")}.urls'

WSGI_APPLICATION = f'{config("ChatServerPlayground")}.wsgi.application'

ASGI_APPLICATION = f'{config("ChatServerPlayground")}.routing.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': config("film_chat_dev"),
        'USER': config("django"),
        'PASSWORD': config("M0vi@D1@ng01"),
        'HOST': 'localhost',
        'PORT': '',
    }
}

AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = config('AWS_STORAGE_BUCKET_NAME')
AWS_S3_ENDPOINT_URL = config('AWS_S3_ENDPOINT_URL')
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}
AWS_LOCATION = config('AWS_LOCATION')

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

#STATIC_ROOT = os.path.join(BASE_DIR, 'static/')
STATIC_URL = 'https://%s/%s/' % (AWS_S3_ENDPOINT_URL, AWS_LOCATION)
TEMP = os.path.join(BASE_DIR, 'temp')
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
EMAIL_PORT = 587
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'matt@gmail.com


BASE_URL = "https://172.31.41.234"
