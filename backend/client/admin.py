from django.contrib import admin
from .models import Client


class ClientAdmin(admin.ModelAdmin):
    search_fields = ('company_name', 'email')
    list_display = ['company_name', 'email', 'is_prospect','sales_contact_id']
    list_filter = ['is_prospect']

admin.site.register(Client, ClientAdmin)