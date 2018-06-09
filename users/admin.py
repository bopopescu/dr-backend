from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from django.utils.translation import gettext, gettext_lazy as _

from .models import User

class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'user_name', 'is_active', 'is_admin', 'phone', 'date_joined', 'last_login', 'avatar')
    list_filter = ('is_admin', 'is_active')
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('user_name',   'email','phone','avatar')}),
        (_('Permissions'), {'fields': ('is_active', 'is_admin')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2','avatar'),
        }),
    )

# Register your models here.
admin.site.unregister(Group)
admin.site.register(User, UserAdmin)
