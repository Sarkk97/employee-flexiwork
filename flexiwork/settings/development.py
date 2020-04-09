from datetime import timedelta
from .base import *


INSTALLED_APPS += ['rest_framework_swagger']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=1)
}

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
# MEDIA_URL = '/media/'
MEDIA_URL = 'http://www.example.com/media/'

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'