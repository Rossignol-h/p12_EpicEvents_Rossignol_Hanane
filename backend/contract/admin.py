from django.contrib import admin
from django import forms

from .models import Contract, ContractStatus
from client.models import Client


# ======================================================== CUSTOM MODEL FORM


class ContractAdminForm(forms.ModelForm):
    class Meta:
        model = Contract
        fields = '__all__'

    def save(self, request, obj, form, change):
        obj.sales_contact = request.user
        obj.save()
        if obj.status == 'True':
            ContractStatus.objects.create(contract=obj)
            Client.objects.update(id=str(obj.client.id), is_prospect= "False")

# ======================================================== CUSTOM ADMIN PAGE


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

# ======================================================== RESTRICT PERMISSION


    def has_change_permission(self, request, obj=None):
        """
            Only the sales employee in charge of the current contract, 
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



class ContractStatusAdmin(admin.ModelAdmin):
    search_fields = ('contract',)
    list_display = ['contract',]
    list_filter = ['contract']

admin.site.register(Contract, ContractAdmin)
admin.site.register(ContractStatus, ContractStatusAdmin)
