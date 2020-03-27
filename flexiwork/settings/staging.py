from .base import *

#ALLOWED_HOSTS = []
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_ROOT'),
	    'PASSWORD': config('DB_PASSWORD'),
	    'HOST': config('DB_HOST'),
    }
}

# MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
# MEDIA_URL = '/media/'