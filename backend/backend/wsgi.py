"""
WSGI config for backend project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
from opentelemetry.instrumentation.auto_instrumentation import initialize

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
from django.conf import settings

application = get_wsgi_application()

if settings.AUTO_INSRUMENT:
    initialize()
