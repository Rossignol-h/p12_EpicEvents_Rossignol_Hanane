from django.contrib import admin
from .models import Client


class ClientAdmin(admin.ModelAdmin):
    search_fields = ('company_name', 'email')
    list_display = ['company_name', 'email', 'is_prospect','sales_contact']
    list_filter = ['is_prospect']

# ======================================================== RESTRICT PERMISSION


    def has_change_permission(self, request, obj=None):
        """
            Only the sales employee in charge of the current client, 
            or manager
            can update it.
        """
        if request.user.role == 'sales':
            if obj is not None and obj.sales_contact == request.user:
                return True
        elif request.user.is_superuser:
            return True
        else:
            return False

admin.site.register(Client, ClientAdmin)