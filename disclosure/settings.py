import os
import os.path as op

import calaccess_raw

BASE_DIR = op.dirname(__file__)
REPO_DIR = op.join(BASE_DIR, os.pardir)
SECRET_KEY = 'w11nbg_3n4+e@qk^b55qgo5qygesn^3=&s1kwtlbpkai$(1jv3'
DEBUG = True
TEMPLATE_DEBUG = True
ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
]
STATIC_ROOT = op.join(REPO_DIR, "static")
MEDIA_ROOT = op.join(REPO_DIR, "media")

# Set this to the path where cronrunner.py is dumping its logs, or "None" to
# imply that this machine will not be runinng cronjobs.
CRON_LOGS_DIR = None

# Set CALACCESS_TEST_DOWNLOAD_DIR for testing calaccess data commands.
_calaccess_repo_dir = op.join(op.dirname(calaccess_raw.__file__),
                              os.pardir)
CALACCESS_TEST_DOWNLOAD_DIR = op.join(_calaccess_repo_dir,
                                      'example', 'test-data')

CALACCESS_DOWNLOAD_DIR = op.join(REPO_DIR, 'data', 'calaccess')
NETFILE_DOWNLOAD_DIR = op.join(REPO_DIR, 'data', 'netfile')


INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',
    'rest_framework',
    'rest_framework_swagger',
    'corsheaders',
    'calaccess_raw',
    'netfile_raw',
    'zipcode_metro_raw',
    'locality',  # dep: none
    'ballot',  # dep: locality
    'finance',  # dep: locality, ballot
    'election_day',  # dep: ballot
    'disclosure'  # dep: locality, ballot, finance
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

CORS_ORIGIN_ALLOW_ALL = True
ROOT_URLCONF = 'disclosure.urls'
WSGI_APPLICATION = 'disclosure.wsgi.application'
REST_FRAMEWORK = {
    'VIEW_NAME_FUNCTION': ('disclosure.swagger_nickname.view_name')
}

DATABASES = {
    'default': {
        'NAME': 'opendisclosure',
        'PASSWORD': '',
        'ENGINE': 'django.db.backends.mysql',
        'USER': 'root',
        'HOST': 'localhost',
        'PORT': '3306',
        'OPTIONS': {
            'local_infile': 1,
        },
    },
    'calaccess_raw': {
        'NAME': 'calaccess_raw',
        'PASSWORD': '',
        'ENGINE': 'django.db.backends.mysql',
        'USER': 'root',
        'HOST': 'localhost',
        'PORT': '3306',
        'OPTIONS': {
            'local_infile': 1,
        },
    },
}

DATABASE_ROUTERS = ['disclosure.routers.DisclosureRouter']

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True
STATIC_URL = '/static/'
MEDIA_URL = '/media/'

_script_dir = op.dirname(__file__)
_settings_local_path = op.join(_script_dir, 'settings_local.py')
if op.exists(_settings_local_path):
    with open(_settings_local_path) as fp:
        exec(fp.read())  # allow errors to be caught.
