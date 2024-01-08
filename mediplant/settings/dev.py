from .base import *
MEDIA_URL = "/media/"
MEDIA_ROOT = '/home/mobiniqow/IdeaProjects/mediplant/media/'

DEBUG = True
STATIC_URL = '/static/'
# STATIC_ROOT = os.path.join(BASE_DIR,"static")
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]
