from .base import *
from dotenv import load_dotenv
load_dotenv()

DOMAIN = os.getenv('DOMAIN')
SECRET_KEY = os.getenv('SECRET_KEY')
IP_ADDRESS = os.getenv('IP_ADDRESS')

DATABASES = {
        'default': {
            # In production we use postgresql
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': os.getenv('DB_NAME'),
            'USER': os.getenv('DB_USER'),
            'PASSWORD': os.getenv('DB_PASSWORD'),
            # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
            'HOST': 'localhost',
            'PORT': '',                      # Set to empty string for default.
        }
    }

DEBUG = False

ALLOWED_HOSTS = [IP_ADDRESS, DOMAIN, 'localhost']

SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True


CSRF_TRUSTED_ORIGINS = ['https://' + DOMAIN]


try:
    from .local import *
except ImportError:
    pass
