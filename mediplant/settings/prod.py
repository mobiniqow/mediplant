from datetime import timedelta

from .base import *

ALLOWED_HOSTS = ["*"]
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'mediplant',
        'USER': 'postgres',
        'PASSWORD': '1423joh89ydfas!@#$djkafsk',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

MEDIA_URL = "/media/"
MEDIA_ROOT = '/var/www/html/mediplant/media'

STATIC_URL = '/static/'
STATIC_ROOT = '/var/www/html/mediplant/static'

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
