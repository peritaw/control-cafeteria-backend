"""
WSGI config for core project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

import sys
try:
    application = get_wsgi_application()
except Exception as e:
    print(f"Error loading WSGI application: {e}", file=sys.stderr)
    raise e

app = application
