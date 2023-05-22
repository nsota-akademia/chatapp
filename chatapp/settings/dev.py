import os

from .base import *  
from .utils import strtobool



DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.getenv("DB_NAME"),
        'USER': os.getenv("DB_USERNAME"),
        'PASSWORD': os.getenv("DB_PASSWORD"),
        'HOST': "localhost",
        'PORT': "5432",
        }
}

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
