from pathlib import Path

import environ
from kombu import Queue

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
    'django.contrib.sites',
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

# Media Storage

AWS_STORAGE_BUCKET_NAME = env('AWS_STORAGE_BUCKET_NAME')
AWS_DEFAULT_ACL = None
AWS_CLOUDFRONT_DOMAIN = env('AWS_CLOUDFRONT_DOMAIN')
AWS_S3_CUSTOM_DOMAIN = AWS_CLOUDFRONT_DOMAIN
AWS_S3_OBJECT_PARAMETERS = {'CacheControl': 'max-age=86400'}
PUBLIC_MEDIA_LOCATION = 'media'
MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/'
DEFAULT_FILE_STORAGE = 'djangito.storages.PublicMediaStorage'
AWS_QUERYSTRING_AUTH = False

DEFAULT_FROM_EMAIL = env('DEFAULT_FROM_EMAIL')

"""
Third Party Settings
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

# Celery Settings

CELERY_BROKER_URL = env('CELERY_BROKER_URL', default='amqp://localhost')
if CELERY_BROKER_URL:
    CELERYD_TASK_SOFT_TIME_LIMIT = 60
    CELERY_ACCEPT_CONTENT = ['application/json']
    CELERY_TASK_SERIALIZER = 'json'
    CELERY_RESULT_SERIALIZER = 'json'
    CELERY_RESULT_BACKEND = env('REDIS_URL', 'redis://localhost:6379/0')
    CELERY_DEFAULT_QUEUE = 'default'
    CELERY_QUEUES = (
        Queue('default'),
    )
    CELERY_CREATE_MISSING_QUEUES = True

# Debug Toolbar Settings
def show_toolbar(request):
    """Callback needed for enabling debug_toolbar"""
    _ = request
    return True


if DEBUG:
    INSTALLED_APPS += ['debug_toolbar']
    MIDDLEWARE = ['debug_toolbar.middleware.DebugToolbarMiddleware'] + MIDDLEWARE
    DEBUG_TOOLBAR_CONFIG = {
        "SHOW_TOOLBAR_CALLBACK": show_toolbar,
    }
    INTERNAL_IPS = ['127.0.0.1']

# AllAuth Settings
AUTHENTICATION_BACKENDS += [
    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
]

ACCOUNT_ADAPTER = 'usermodel.adapters.MyAccountAdapter'
SOCIALACCOUNT_ADAPTER = 'usermodel.adapters.MySocialAccountAdapter'
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
EMAIL_BACKEND = 'post_office.EmailBackend'

POST_OFFICE = {
    'BACKENDS': {
        'default': 'django_ses.SESBackend',
    },
    'DEFAULT_PRIORITY': 'now',
}

# AWS SES Settings
AWS_ACCESS_KEY_ID = env('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = env('AWS_SECRET_ACCESS_KEY')
AWS_SES_REGION_NAME = env('AWS_SES_REGION_NAME', default='us-east-2')
AWS_SES_REGION_ENDPOINT = env('AWS_SES_REGION_ENDPOINT', default='email.us-east-2.amazonaws.com')
AWS_SES_CONFIGURATION_SET = env('AWS_SES_CONFIGURATION_SET', default='Engagement')
