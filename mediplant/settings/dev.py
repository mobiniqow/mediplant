from .base import *

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

DEBUG = True
STATIC_URL = '/static/'
# STATIC_ROOT = os.path.join(BASE_DIR,"static")
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]
DATA_UPLOAD_MAX_NUMBER_FIELDS = 20003
