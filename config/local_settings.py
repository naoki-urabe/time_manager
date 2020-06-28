import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '09u+)!uq6j2yk@ngr36c($j4h3h(=rfjd7_&8v=rlv4(uu+b-q'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'time_manager',
        'USER': 'nao',
        'PASSWORD': 'fg47gh62',
        'HOST': 'localhost',
        'PORT': ''
    }
}

DEBUG = True