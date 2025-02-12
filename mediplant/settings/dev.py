import os
from datetime import timedelta

from .base import *

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")
DEBUG = True
STATIC_URL = '/static/'
# STATIC_ROOT = os.path.join(BASE_DIR,"static")
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]
# print([os.path.join(BASE_DIR, "static")])
DATA_UPLOAD_MAX_NUMBER_FIELDS = 20003
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 16,
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}
CORS_ALLOW_ALL_ORIGINS = True
INTERNAL_IPS = [
    "127.0.0.1",
]

MERCHANT_ID = "5ed2e796-0448-40db-920c-1df64ddb0551"
CALLBACK_URL = "http://localhost:8000/transaction/payment/verify/"

TAILWIND_APP_NAME = 'theme'
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

APPEND_SLASH=True
