from configurations import values

from djangitos.settings import BaseConfig

# Temporary solution to make sure Django picks up the default auto_field.
# Model checks are performed before django-configurations are instantiated
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


class ProjectConfig(BaseConfig):
    PROJECT_APPS = BaseConfig.PROJECT_APPS + [
        # add your apps here
    ]
    SOCIALACCOUNT_GOOGLE_CLIENT_ID = values.Value()
    SOCIALACCOUNT_GOOGLE_CLIENT_SECRET = values.Value()

    @property
    def SOCIALACCOUNT_PROVIDERS(self):
        return {
            'google': {
                'SCOPE': [
                    'profile',
                    'email',
                ],
                # For each OAuth based provider, either add a ``SocialApp``
                # (``socialaccount`` app) containing the required client
                # credentials, or list them here:
                'APP': {
                    'client_id': self.SOCIALACCOUNT_GOOGLE_CLIENT_ID,
                    'secret': self.SOCIALACCOUNT_GOOGLE_CLIENT_SECRET,
                    'key': ''
                }
            }
        }
