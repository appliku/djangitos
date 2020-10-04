from pathlib import Path

import environ


env = environ.Env()

"""
Project Settings
"""

BASE_DIR = Path(__file__).resolve(strict=True).parent.parent

DEBUG = env.bool('DJANGO_DEBUG', default=False)

# Allowed Hosts Definition
if DEBUG:
    # If Debug is True, allow all.
    ALLOWED_HOSTS = ['*']
else:
    ALLOWED_HOSTS = env.list('DJANGO_ALLOWED_HOSTS', default=['example.com'])

SECRET_KEY = env('DJANGO_SECRET_KEY')

"""
Project Apps Definitions
Django Apps - Django Internal Apps
Third Party Apps - Apps installed via requirements.txt
Project Apps - Project owned / created apps

Installed Apps = Django Apps + Thrid Part apps + Projects Apps
"""
DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

THRID_PARTY_APPS = [
    'import_export',
    'django_extensions',
    'rest_framework',
    'corsheaders',
    'djangoql',
]

PROJECT_APPS = [
    'usermodel',
]

INSTALLED_APPS = DJANGO_APPS + THRID_PARTY_APPS + PROJECT_APPS

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Databases
DATABASES = {
    "default": env.db("DATABASE_URL")
}
DATABASES["default"]["ATOMIC_REQUESTS"] = True
DATABASES["default"]["CONN_MAX_AGE"] = env.int("CONN_MAX_AGE", default=60)

ROOT_URLCONF = 'djangito.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'djangito.wsgi.application'

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# User Model Definition
AUTH_USER_MODEL = 'usermodel.User'

# Static files and Media Files Definition
STATICFILES_STORAGE = 'djangito.storages.WhiteNoiseStaticFilesStorage'

STATIC_ROOT = BASE_DIR / 'staticfiles'
STATIC_HOST = env('DJANGO_STATIC_HOST', default='')
STATIC_URL = STATIC_HOST + '/static/'

TIME_ZONE = 'UTC'
LANGUAGE_CODE = 'en-us'
SITE_ID = 1
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Admin URL Definition
ADMIN_URL = env('DJANGO_ADMIN_URL', default='admin/')

"""
Thrid Party Settings
"""
# Sentry Settings
SENTRY_DSN = env('SENTRY_DSN', default=None)

if SENTRY_DSN:
    import sentry_sdk
    from sentry_sdk.integrations.django import DjangoIntegration
    from sentry_sdk.integrations.celery import CeleryIntegration
    from sentry_sdk.integrations.redis import RedisIntegration

    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=[
            DjangoIntegration(),
            CeleryIntegration(),
            RedisIntegration()
        ],

        # If you wish to associate users to errors (assuming you are using
        # django.contrib.auth) you may enable sending PII data.
        send_default_pii=True
    )

# Whitenose Settings
# WHITENOISE_AUTOREFRESH = DEBUG -> Default behavior.
# http://whitenoise.evans.io/en/stable/django.html#WHITENOISE_AUTOREFRESH
WHITENOISE_USE_FINDERS = True

# Redis Settings
REDIS_URL = env('REDIS_URL', default=None)

if REDIS_URL:
    CACHES = {
        "default": env.cache('REDIS_URL')
    }
