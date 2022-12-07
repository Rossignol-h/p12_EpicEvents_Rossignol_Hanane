from django.contrib import admin
from .models import Contract, ContractStatus
from client.models import Client


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
        ('Employee in charge', {'fields': ('sales_contact',)}),
        ('Choose the client of this contract', {'fields': ('client',)}),
        ('This contract is signed ?', {'fields': ('status',)}),
    )
    actions = [make_signed]

    def save(self, request, obj, form, change):
        obj.sales_contact = request.user
        obj.save()
        if obj.status == 'True':
            ContractStatus.objects.create(contract=obj)
            Client.objects.update(id=str(obj.client.id), is_prospect= "False")





    def save(self, commit=True):
        contract = super().save(commit=False)
        contract.sales_contact = self.cleaned_data['client'].sales_contact
        if commit:
            contract.save()
        return contract


class ContractStatusAdmin(admin.ModelAdmin):
    search_fields = ('contract',)
    list_display = ['contract',]
    list_filter = ['contract']

admin.site.register(Contract, ContractAdmin)
admin.site.register(ContractStatus, ContractStatusAdmin)
