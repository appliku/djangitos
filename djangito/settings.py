from pathlib import Path
import environ
import os

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

Installed Apps = Django Apps + Third Part apps + Projects Apps
"""
DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.sites',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.redirects',
]

THIRD_PARTY_APPS = [
    'import_export',
    'django_extensions',
    'rest_framework',
    'storages',
    'corsheaders',
    'djangoql',
    'post_office',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'crispy_forms',
]

PROJECT_APPS = [
    'usermodel',
    'ses_sns',
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + PROJECT_APPS

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.redirects.middleware.RedirectFallbackMiddleware',
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
        'DIRS': [BASE_DIR / 'templates'],
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
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]
# User Model Definition
AUTH_USER_MODEL = 'usermodel.User'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
TIME_ZONE = 'UTC'
LANGUAGE_CODE = 'en-us'
SITE_ID = 1
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Admin URL Definition
ADMIN_URL = env('DJANGO_ADMIN_URL', default='admin/')

# Redis Settings
REDIS_URL = env('REDIS_URL', default=None)

if REDIS_URL:
    CACHES = {
        "default": env.cache('REDIS_URL')
    }
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler'
        },
    },
    'loggers': {
        '': {  # 'catch all' loggers by referencing it with the empty string
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    },
}

# Static And Media Settings
AWS_STORAGE_BUCKET_NAME = env('AWS_STORAGE_BUCKET_NAME', default=None)
if AWS_STORAGE_BUCKET_NAME:
    AWS_DEFAULT_ACL = None
    AWS_QUERYSTRING_AUTH = False
    AWS_S3_CUSTOM_DOMAIN = env('AWS_S3_CUSTOM_DOMAIN', default=None) or f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
    AWS_S3_OBJECT_PARAMETERS = {'CacheControl': 'max-age=600'}

    # s3 static settings
    STATIC_LOCATION = 'static'
    STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{STATIC_LOCATION}/'
    STATICFILES_STORAGE = 'djangito.storages.StaticStorage'

    # s3 public media settings
    PUBLIC_MEDIA_LOCATION = 'media'
    MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{PUBLIC_MEDIA_LOCATION}/'
    DEFAULT_FILE_STORAGE = 'djangito.storages.PublicMediaStorage'

    STATICFILES_DIRS = (
        # os.path.join(BASE_DIR, "static"),
    )
else:
    MIDDLEWARE.insert(2, 'whitenoise.middleware.WhiteNoiseMiddleware')
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'
    WHITENOISE_USE_FINDERS = True
    STATIC_HOST = env('DJANGO_STATIC_HOST', default='')
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
    STATIC_URL = STATIC_HOST + '/static/'
    if DEBUG:
        WHITENOISE_AUTOREFRESH = True
DEFAULT_FROM_EMAIL = env('DEFAULT_FROM_EMAIL', default='test@example.com')

"""
Third Party Settings
"""

# Honeybadger Settings
HONEYBADGER_API_KEY = env('HONEYBADGER_API_KEY', default=None)
if HONEYBADGER_API_KEY:
    MIDDLEWARE = ['honeybadger.contrib.DjangoHoneybadgerMiddleware'] + MIDDLEWARE
    HONEYBADGER = {
        'API_KEY': HONEYBADGER_API_KEY
    }

# Celery Settings
try:
    from kombu import Queue
    from celery import Celery

    CELERY_BROKER_URL = env('CELERY_BROKER_URL', default='amqp://localhost')
    if CELERY_BROKER_URL:
        CELERYD_TASK_SOFT_TIME_LIMIT = 60
        CELERY_ACCEPT_CONTENT = ['application/json']
        CELERY_TASK_SERIALIZER = 'json'
        CELERY_RESULT_SERIALIZER = 'json'
        CELERY_RESULT_BACKEND = env('REDIS_URL', default='redis://localhost:6379/0')
        CELERY_DEFAULT_QUEUE = 'default'
        CELERY_QUEUES = (
            Queue('default'),
        )
        CELERY_CREATE_MISSING_QUEUES = True
except ModuleNotFoundError:
    print("Celery/kombu not installed. Skipping...")

# AllAuth Settings
AUTHENTICATION_BACKENDS += [
    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
]

ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
ACCOUNT_FORMS = {'signup': 'usermodel.forms.MyCustomSignupForm'}
ACCOUNT_MAX_EMAIL_ADDRESSES = 2
SOCIALACCOUNT_PROVIDERS = {

}
SOCIALACCOUNT_PROVIDERS_GOOGLE_CLIENT_ID = env('SOCIALACCOUNT_PROVIDERS_GOOGLE_CLIENT_ID', default=None)
if SOCIALACCOUNT_PROVIDERS_GOOGLE_CLIENT_ID:
    SOCIALACCOUNT_PROVIDERS['google'] = {
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        },
        # For each OAuth based provider, either add a ``SocialApp``
        # (``socialaccount`` app) containing the required client
        # credentials, or list them here:
        'APP': {
            'client_id': SOCIALACCOUNT_PROVIDERS_GOOGLE_CLIENT_ID,
            'secret': env('SOCIALACCOUNT_PROVIDERS_GOOGLE_SECRET'),
        }
    }
# Crispy Forms Settings
CRISPY_TEMPLATE_PACK = 'bootstrap4'

# Django Post Office Settings
EMAIL_BACKEND = 'ses_sns.backend.FilteringEmailBackend'

POST_OFFICE = {
    'BACKENDS': {
        'default': 'django_ses.SESBackend',
    },
    'DEFAULT_PRIORITY': 'now',
}

# AWS SES Settings

AWS_SES_REGION_NAME = env('AWS_SES_REGION_NAME', default='us-east-1')
AWS_SES_REGION_ENDPOINT = env('AWS_SES_REGION_ENDPOINT', default='email.us-east-1.amazonaws.com')
AWS_SES_CONFIGURATION_SET = env('AWS_SES_CONFIGURATION_SET', default=None)
