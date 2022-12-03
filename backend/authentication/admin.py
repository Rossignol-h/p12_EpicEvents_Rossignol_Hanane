from django.contrib.auth.admin import UserAdmin
from django.contrib import admin

from .models import Employee


class CustomUserAdmin(UserAdmin):

    search_fields = ('email',)
    list_display = ['email', 'role', 'phone_number', 'is_superuser']
    list_filter = ['role',]

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1','password2' ),
        }),
    )

    fieldsets = (
        (None, {'fields': ('email',)}),
        ('Contact', {'fields': ('phone_number',)}),
        ('Security', {'fields': ('password',)}),
        ('Permissions', {'fields': ('role',)}),
    )

    radio_fields = {'role': admin.HORIZONTAL}
    ordering = ('email',)

admin.site.register(Employee, CustomUserAdmin)