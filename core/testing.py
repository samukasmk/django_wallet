from core.settings import *

DEBUG = True
TESTING_MODE = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': f'{BASE_DIR}/db-unit-tests.sqlite3',
    }
}