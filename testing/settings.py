import os

AUTHNET_LOGIN_ID = ''
AUTHNET_TRANSACTION_KEY = ''

SECRET_KEY="testing"

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3'
    },
}

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.staticfiles',
    'kaggregate',
    'kaggregate.tests',
]

LANGUAGE_CODE = 'en'

LOGIN_URL = '/accounts/login/'

MANAGERS = []

MIDDLEWARE_CLASSES = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.common.CommonMiddleware',
]

ROOT_URLCONF = 'testing.urls'

SITE_ID = 1

TEMPLATE_DIRS = [os.path.join(os.path.dirname(__file__), 'templates')]

TEST_RUNNER = 'testing.NoseTestSuiteRunner'

USE_I18N = True
