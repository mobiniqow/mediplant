from datetime import timedelta

from .base import *

ALLOWED_HOSTS = ["*"]
DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'mediplant_db',
        'USER': 'mediplant_user',
        'PASSWORD': '1423joh89ydfas!@#$djkafsk',
        'HOST': 'db',
        'PORT': '5432',
    }
}

MEDIA_URL = "/media/"
MEDIA_ROOT = '/var/html/www/mediplant/media'

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

import os

GDAL_LIBRARY_PATH = os.getenv('GDAL_LIBRARY_PATH', '/usr/lib/libgdal.so')

if GDAL_LIBRARY_PATH:
    os.environ['GDAL_LIBRARY_PATH'] = GDAL_LIBRARY_PATH

