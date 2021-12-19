import os
from pathlib import Path
from configurations import Configuration, values


class BaseConfig(Configuration):
    BASE_DIR = Path(__file__).resolve(strict=True).parent.parent
    DEBUG = values.BooleanValue(False)
    ALLOWED_HOSTS = values.ListValue()
    SECRET_KEY = values.SecretValue()
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
        'tailwind',
    ]

    PROJECT_APPS = [
        'usermodel',
        'ses_sns',
        'theme',
        'demo',
    ]

    @property
    def INSTALLED_APPS(self):
        return self.DJANGO_APPS + self.THIRD_PARTY_APPS + self.PROJECT_APPS

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
    DATABASE_URL = values.DatabaseURLValue('postgres://djangitos:djagitos@db/djangitos')  # type: dict

    @property
    def DATABASES(self):
        databases = dict(self.DATABASE_URL)
        databases['default']["ATOMIC_REQUESTS"] = True
        databases['default']["CONN_MAX_AGE"] = 60
        return databases

    ROOT_URLCONF = values.Value('project.urls')

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

    WSGI_APPLICATION = 'project.wsgi.application'

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
        'allauth.account.auth_backends.AuthenticationBackend',
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
    ADMIN_URL = values.Value('admin/')

    # Redis Settings
    REDIS_URL = values.Value(environ_prefix=None)

    CACHE_URL = values.CacheURLValue()
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

    # STATIC AND MEDIA Settings
    AWS_DEFAULT_ACL = None
    AWS_QUERYSTRING_AUTH = False
    AWS_S3_OBJECT_PARAMETERS = {'CacheControl': 'max-age=300'}
    WHITENOISE_USE_FINDERS = True

    @property
    def WHITENOISE_AUTOREFRESH(self):
        return self.DEBUG

    STATIC_MODE = values.Value('whitenoise')  # can be 'whitenoise' or 's3'

    STATIC_S3_ACCESS_KEY_ID = values.Value()
    STATIC_S3_SECRET_ACCESS_KEY = values.Value()
    STATIC_S3_BUCKET_NAME = values.Value()
    STATIC_S3_PATH = values.Value('static')
    STATIC_S3_CUSTOM_DOMAIN = values.Value()
    STATIC_HOST = values.Value('')
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

    @property
    def STATIC_S3_DOMAIN(self):
        if self.STATIC_S3_CUSTOM_DOMAIN:
            return self.STATIC_S3_CUSTOM_DOMAIN
        return f'{self.STATIC_S3_BUCKET_NAME}.s3.amazonaws.com'

    @property
    def STATICFILES_STORAGE(self):
        if self.STATIC_MODE == 's3':
            return 'djangitos.storages.StaticStorage'
        return 'whitenoise.storage.CompressedStaticFilesStorage'

    @property
    def STATIC_URL(self):
        if self.STATIC_MODE == 's3':
            return f'https://{self.STATIC_S3_DOMAIN}/{self.STATIC_S3_PATH}/'
        return f'{self.STATIC_HOST}/static/'

    MEDIA_MODE = values.Value()  # 's3'
    MEDIA_S3_ACCESS_KEY_ID = values.Value()
    MEDIA_S3_SECRET_ACCESS_KEY = values.Value()
    MEDIA_S3_BUCKET_NAME = values.Value()
    MEDIA_S3_PATH = values.Value('media')
    MEDIA_S3_CUSTOM_DOMAIN = values.Value()
    MEDIA_HOST = values.Value('')
    DEFAULT_FILE_STORAGE = 'djangitos.storages.PublicMediaStorage'

    @property
    def MEDIA_S3_DOMAIN(self):
        if self.MEDIA_S3_CUSTOM_DOMAIN:
            return self.MEDIA_S3_CUSTOM_DOMAIN
        return f'{self.MEDIA_S3_BUCKET_NAME}.s3.amazonaws.com'

    @property
    def MEDIA_URL(self):
        return f'https://{self.MEDIA_S3_DOMAIN}/{self.MEDIA_S3_PATH}/'

    DEFAULT_FROM_EMAIL = values.Value()

    # Error Tracking
    HONEYBADGER_API_KEY = values.Value(environ_prefix=None)

    @property
    def HONEYBADGER(self):
        return {
            'API_KEY': self.HONEYBADGER_API_KEY
        }

    # Celery Settings
    CELERY_BROKER_URL = values.Value('amqp://localhost', environ_prefix=None)
    CELERYD_TASK_SOFT_TIME_LIMIT = 60
    CELERY_ACCEPT_CONTENT = ['application/json']
    CELERY_TASK_SERIALIZER = 'json'
    CELERY_RESULT_SERIALIZER = 'json'
    CELERY_RESULT_BACKEND = REDIS_URL
    CELERY_TASK_DEFAULT_QUEUE = 'default'
    CELERY_CREATE_MISSING_QUEUES = True

    # Django All Auth Settings
    ACCOUNT_USER_MODEL_USERNAME_FIELD = None
    ACCOUNT_EMAIL_REQUIRED = True
    ACCOUNT_USERNAME_REQUIRED = False
    ACCOUNT_AUTHENTICATION_METHOD = 'email'
    ACCOUNT_UNIQUE_EMAIL = True
    ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
    ACCOUNT_FORMS = {'signup': 'usermodel.forms.MyCustomSignupForm'}
    ACCOUNT_MAX_EMAIL_ADDRESSES = 2
    ACCOUNT_DEFAULT_HTTP_PROTOCOL = 'https'

    # Crispy Forms Settings
    CRISPY_ALLOWED_TEMPLATE_PACKS = 'tailwind'
    CRISPY_TEMPLATE_PACK = 'tailwind'

    EMAIL_BACKEND = 'ses_sns.backend.FilteringEmailBackend'

    POST_OFFICE = {
        'BACKENDS': {
            'default': 'django_ses.SESBackend',
        },
        'CELERY_ENABLED': True,
        'DEFAULT_PRIORITY': 'now',
    }

    # AWS SES Settings

    AWS_SES_REGION_NAME = values.Value('us-east-1', environ_prefix=None)
    AWS_SES_REGION_ENDPOINT = values.Value('email.us-east-1.amazonaws.com', environ_prefix=None)
    AWS_SES_CONFIGURATION_SET = values.Value(environ_prefix=None)

    # Django Tailwind Settings
    TAILWIND_APP_NAME = 'theme'
