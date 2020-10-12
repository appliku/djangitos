from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.utils.crypto import get_random_string

User = get_user_model()


class Command(BaseCommand):
    def handle(self, *args, **options):
        try:
            u = None
            if not User.objects.filter(email='admin@example.com').exists() and not User.objects.filter(
                    is_superuser=True).exists():
                print("admin user not found, creating one")
                email = 'admin@example.com'
                new_password = get_random_string()

                u = User.objects.create_superuser(email, new_password)
                print(f"===================================")
                print(f"A superuser was created with email {email} and password {new_password}")
                print(f"===================================")
            else:
                print("admin user found. Skipping super user creation")
            print(u)
        except Exception as e:
            print(f"There was an error: {e}")
