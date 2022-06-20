from .base import *
from dotenv import load_dotenv

load_dotenv()


SECRET_KEY = os.getenv('SECRET_KEY')

DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
            'NAME': os.getenv('DB_NAME'),                      # Or path to database file if using sqlite3.
            'USER': os.getenv('DB_USER'),
            'PASSWORD': os.getenv('DB_PASSWORD'),
            'HOST': 'localhost',                      # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
            'PORT': '',                      # Set to empty string for default.
        }
    }

DEBUG = False

ALLOWED_HOSTS= ['139.162.184.175', "wagtail-italia.it", 'localhost']

SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True


CSRF_TRUSTED_ORIGINS = ['https://wagtail-italia.it']


try:
    from .local import *
except ImportError:
    pass
