"""
WSGI config for flexiwork project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/howto/deployment/wsgi/
"""

import os
from decouple import config
from django.core.wsgi import get_wsgi_application

if config('ENVIRONMENT') == 'staging':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'flexiwork.settings.staging')
else:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'flexiwork.settings.production')
application = get_wsgi_application()
