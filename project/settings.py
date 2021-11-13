from configurations import values

from djangitos.settings import BaseConfig


class ProjectConfig(BaseConfig):
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
