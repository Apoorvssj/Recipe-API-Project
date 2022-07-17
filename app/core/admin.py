from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# just to support auto langiage change
from django.utils.translation import gettext_lazy as _

from core import models

# Register your models here.


class UserAdmin(BaseUserAdmin):
    """Define the admin pages for users."""
    ordering = ['id']
    list_display = ['email', 'name']
    # overrides all the fields on details page of
    # BaseUserAdmin(default user model)
    fieldsets = (
        (None, {'fields': ('email', 'password',)}),
        (
            _('Permissions'),
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                )
            }
        ),
        (_('Important dates'), {'fields': ('last_login',)}),
    )
    readonly_fields = ['last_login']
    # overrides all the fields on add page of
    # BaseUserAdmin(default user model)
    add_fieldsets = (
        (None, {
            'classes': ('wide',),  # css
            'fields': (
                'email',
                'password1',
                'password2',
                'name',
                'is_active',
                'is_staff',
                'is_superuser',
            )
        }),
    )


admin.site.register(models.User, UserAdmin)
