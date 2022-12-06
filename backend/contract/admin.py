from django.contrib import admin
from .models import Contract, ContractStatus


@admin.action(description='Mark selected contracts as signed')
def make_signed(modeladmin, request, queryset):
    queryset.update(status='True')

class ContractAdmin(admin.ModelAdmin):
    search_fields = ['date_created', 'amount', 'client__email', 'client__company_name' ]
    list_display = ['id', 'client', 'sales_contact', 'amount', 'date_created', 'status']
    list_filter = ['client', 'payment_due', 'status']
    # set display of form to add contract:
    fieldsets = (
        (None, {'fields': ('amount',)}),
        ('Deadline', {'fields': ('payment_due',)}),
        ('Choose the client of this contract', {'fields': ('client',)}),
        ('This contract is signed ?', {'fields': ('status',)}),
    )
    actions = [make_signed]


class ContractStatusAdmin(admin.ModelAdmin):
    search_fields = ('contract',)
    list_display = ['contract',]
    list_filter = ['contract']
    
    # radio_fields = {'is_signed': admin.HORIZONTAL}

admin.site.register(Contract, ContractAdmin)
admin.site.register(ContractStatus, ContractStatusAdmin)
