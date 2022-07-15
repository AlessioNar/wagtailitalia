"""
WSGI config for wagtailitalia project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/wsgi/
"""

from django.core.wsgi import get_wsgi_application
import os
from dotenv import load_dotenv

load_dotenv()
NAME = os.getenv('NAME')


os.environ.setdefault("DJANGO_SETTINGS_MODULE",
                      NAME + ".settings.production")

application = get_wsgi_application()
