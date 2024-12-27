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
