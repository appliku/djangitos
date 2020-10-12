from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from usermodel.models import User
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin


@admin.register(User)
class UserAdmin(DefaultUserAdmin):
    fieldsets = (
        (
            None,
            {
                'fields': (
                    'email', 'password'
                )
            }
        ),
        (
            _('Permissions'),
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                    'groups',
                    'user_permissions',
                ),
            }
        ),
        (
            _('Important dates'),
            {
                'fields': (
                    'last_login',
                    'date_joined',
                )
            }
        ),
        (
            _('User data'),
            {
                'fields': (
                    ('is_email_confirmed',),
                )
            }
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': ('email', 'password1', 'password2'),
            }
        ),
    )
    list_display = ('email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('first_name', 'last_name', 'email')
    ordering = ('email',)
