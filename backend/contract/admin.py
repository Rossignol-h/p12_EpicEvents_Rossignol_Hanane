from django.contrib import admin
from django import forms

from .models import Contract, ContractStatus
from event.models import Event
from client.models import Client


# ======================================================== CUSTOM MODEL FORM


class ContractAdminForm(forms.ModelForm):
    class Meta:
        model = Contract
        fields = '__all__'

    # def save(self, request, obj, form, change):
    #     obj.sales_contact = request.user
    #     obj.save()
    #     if obj.status == 'True':
    #         ContractStatus.objects.create(contract=obj)
    #         Event.objects.create(contract=obj, client=obj.client.id)
    #         Client.objects.update(id=str(obj.client.id), is_prospect= "False")



# ======================================================== CUSTOM CONTRACT ADMIN PAGE


@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    form = ContractAdminForm
    search_fields = ['client__email', 'client__company_name', 'date_created', 'amount']
    list_display = ['id', 'client', 'sales_contact', 'amount', 'date_created', 'status']
    list_filter = ['client', 'payment_due', 'status']
    readonly_fields = ['date_created', 'date_updated',]

    # set display of form to add contract:
    fieldsets = (
        ('Facturation', {'fields': ('amount',)}),
        ('Deadline', {'fields': ('payment_due',)}),
        ('Employee in charge', {'fields': ('sales_contact',)}),
        ('The client of this contract', {'fields': ('client',)}),
        ('This contract is signed ?', {'fields': ('status',)}),
    )

# ================================================================ SIGNED CONTRACTS MODELADMIN


@admin.register(ContractStatus)
class ContractStatusAdmin(admin.ModelAdmin):
    search_fields = ('contract',)
    list_display = ['contract']
    list_filter = ['contract']


    def get_queryset(self, request):
        """
            Make sure to retrun appropriate queries :
            if the user is superuser(manager) ==> return all signed contracts
            if the user role is sales ==> return only signed contracts, that he is in charge of 
            if the user is support ==> return nothing
        """
        queryset = super().get_queryset(request)
        employee = request.user

        if employee.role == 'sales':
            return ContractStatus.objects.filter(contract__sales_contact=employee)

        elif employee.is_superuser:
            return ContractStatus.objects.all()

        else:
            return queryset.none()
