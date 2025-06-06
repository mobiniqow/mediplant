from datetime import timedelta

from .base import *

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "USER": "postgres",
        "PASSWORD": "ewrasdfwqe",
        "NAME": "mediplant",
        "HOST": "localhost",
        "PORT": "5432",
    }
}
DATA_UPLOAD_MAX_MEMORY_SIZE = 524288000  # 50 MB
FILE_UPLOAD_MAX_MEMORY_SIZE = 524288000

MERCHANT_ID = "5ed2e796-0448-40db-920c-1df64ddb0551"
CALLBACK_URL = "http://localhost:8000/transaction/payment/verify/"
MEDIA_URL = "/media/"
MEDIA_ROOT = '/var/html/www/mediplant/media'

CSRF_TRUSTED_ORIGINS = [
    "https://shopper.mediplant.ir",
    "https://doctor.mediplant.ir",
    "https://mediplant.ir",
    "https://mediplant.org",
    "https://wwww.mediplant.ir",
    "http://localhost:3000",
]

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
# CORS_ALLOW_ALL_ORIGINS = True
# CORS_ALLOW_CREDENTIALS = True
# import os
#
# GDAL_LIBRARY_PATH = os.getenv('GDAL_LIBRARY_PATH', '/usr/lib/libgdal.so')
#
# if GDAL_LIBRARY_PATH:
#     os.environ['GDAL_LIBRARY_PATH'] = GDAL_LIBRARY_PATH


CORS_ALLOWED_ORIGINS = [
    "https://shopper.mediplant.ir",
    "https://doctor.mediplant.ir",
    "https://mediplant.ir",
    "https://mediplant.org",
    "https://wwww.mediplant.ir",
    "http://localhost:3000",
]


# CORS_ALLOW_ALL_ORIGINS = True
# CORS_ALLOW_CREDENTIALS = True
CSRF_COOKIE_SECURE=True

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("127.0.0.1", 6379)],
        },
    },
}
