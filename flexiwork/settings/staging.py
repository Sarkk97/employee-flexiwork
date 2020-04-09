from datetime import timedelta
from .base import *

STAGING_BASE_DIR = '/var/www/PYTHON/flexiwork_backend'

ALLOWED_HOSTS = ['.energy360africa.com']
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
	    'PASSWORD': config('DB_PASSWORD'),
	    'HOST': config('DB_HOST'),
    }
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=6)
}

MEDIA_ROOT = os.path.join(STAGING_BASE_DIR, 'media')
MEDIA_URL = '/media/'

LOGGING = {                                                                                                                 
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'logfile': {
            'class': 'logging.RotatingFileHandler',
            'filename': os.path.join(STAGING_BASE_DIR, 'server.log'),
            'maxBytes': 1024*1024*15, # 15MB
            'backupCount': 10,
        },
    },
    'loggers': {
        'django': {
            'handlers': ['logfile'],
            'level': 'INFO'
        },
    },
}