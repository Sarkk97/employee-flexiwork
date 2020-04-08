from .base import *

ALLOWED_HOSTS = ['energy360africa.com']
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_ROOT'),
	    'PASSWORD': config('DB_PASSWORD'),
	    'HOST': config('DB_HOST'),
    }
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=6)
}

MEDIA_ROOT = '/var/www/PYTHON/flexiwork_backend/media'
MEDIA_URL = '/media/'