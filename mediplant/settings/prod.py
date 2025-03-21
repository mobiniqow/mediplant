from datetime import timedelta

from .base import *

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "USER": "iot_user",
        "PASSWORD": "ewrasdfwqe",
        "NAME": "mediplant",
        "HOST": "localhost",
        "PORT": "5432",
    }
}


MEDIA_URL = "/media/"
MEDIA_ROOT = '/var/html/www/mediplant/media'
CSRF_TRUSTED_ORIGINS = ['https://mediplant.ir', 'https://www.mediplant.ir','http://mediplant.ir','http://www.mediplant.ir']
ALLOWED_HOSTS = ['*']
STATIC_URL = '/static/'
STATIC_ROOT = '/var/html/www/mediplant/static'

# STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=14),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=45),
    "ROTATE_REFRESH_TOKENS": False,
    "BLACKLIST_AFTER_ROTATION": True,
    "ALGORITHM": "HS256",
    "SIGNING_KEY": SECRET_KEY,
    "VERIFYING_KEY": None,
    "AUDIENCE": None,
    "ISSUER": None,
    "AUTH_HEADER_TYPES": ("Bearer",),
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "TOKEN_TYPE_CLAIM": "token_type",
    "JTI_CLAIM": "jti",
    "TOKEN_USER_CLASS": "rest_framework_simplejwt.models.TokenUser",
    "SLIDING_TOKEN_REFRESH_EXP_CLAIM": "refresh_exp",
    "SLIDING_TOKEN_LIFETIME": timedelta(days=99),
    "SLIDING_TOKEN_REFRESH_LIFETIME": timedelta(days=99),
}
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 16,
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True
import os

GDAL_LIBRARY_PATH = os.getenv('GDAL_LIBRARY_PATH', '/usr/lib/libgdal.so')

if GDAL_LIBRARY_PATH:
    os.environ['GDAL_LIBRARY_PATH'] = GDAL_LIBRARY_PATH

