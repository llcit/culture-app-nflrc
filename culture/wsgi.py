"""
WSGI config for culture project.

It exposes the WSGI callable as a culture_content-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/howto/deployment/wsgi/
"""

import os, sys

from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'culture.settings')