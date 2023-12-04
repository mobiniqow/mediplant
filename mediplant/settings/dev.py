from .base import *

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

STATIC_URL = '/static/'
# STATIC_ROOT = os.path.join(BASE_DIR,"static")
print(f'BASE_DIR{BASE_DIR}')
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]
