from django.contrib import admin

from .models import Contract, ContractStatus
from client.models import Client

# ======================================================== CUSTOM CONTRACT ADMIN PAGE


@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    empty_value_display = 'None' # Display None for empty values instead of -
    search_fields = ['client__email', 'client__company_name', 'date_created', 'amount']
    list_display = ['id', 'client', 'sales_contact', 'amount', 'date_created', 'status']
    list_filter = ['client', 'payment_due', 'status']
    readonly_fields = ['date_created', 'date_updated',]

    # set display of form to add contract:
    fieldsets = (
        ('Facturation', {'fields': ('amount',)}),
        ('Deadline', {'fields': ('payment_due',)}),
        ('The client of this contract', {'fields': ('client',)}),
        ('Who is in charge of this contract? ', {'fields': ('sales_contact',)}),
        ('This contract is signed ?', {'fields': ('status',)}),
    )


# ========================================================================


    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """
            Override the queryset of clients in form :
            if user is sales employee:
                Make sure queryset contains only clients who is in charge of.
            if he is superuser (manager):
                return all clients.
        """
        
        if request.user.role == 'sales':
            if db_field.name == "client":
                kwargs["queryset"] = Client.objects.filter(sales_contact=request.user)

        if request.user.is_superuser:
            if db_field.name == "client":
                kwargs["queryset"] = Client.objects.all()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


# ========================================================================

    def get_readonly_fields(self, request, obj=None):
        """
            When updating contract :
                Make sure to avoid a sales employee to change 
                the sales_contact field, and client 
                by adding it to readonly_fields. 
        """
        # 'change' form
        if obj is not None and request.user.role == 'sales':
            return self.readonly_fields + ['sales_contact', 'client']
        # 'add' form
        if obj is None and request.user.role == 'sales':
            return self.readonly_fields + ['sales_contact',]

        else:
            return self.readonly_fields

# ========================================================================


    def save_model(self, request, obj, form, change):
        """
            The sales employee's client is automatically
            the sales contact of this new contract
            + If status of contract is true(signed):
                add it to contractStatus,
                update status' client (is not a propect anymore).
        """
        obj.sales_contact = obj.client.sales_contact
        obj.save()
        if obj.status == True:
            signed_contract = ContractStatus.objects.filter(contract=obj)
            if not signed_contract:
                ContractStatus.objects.create(contract=obj)

            if obj.client:
                obj.client.is_prospect = "False"
                obj.client.save()


# ========================================================================


    def has_change_permission(self, request, obj=None):
        """
            Make sure only a manager or the sales employee 
            in charge of this client 
            can update it
        """
        if request.user.role == 'sales':
            if obj is not None and request.user == obj.sales_contact:
                return True
            return False

        elif request.user.is_superuser:
            return True
        return False

# ================================================================ SIGNED CONTRACTS MODELADMIN


@admin.register(ContractStatus)
class ContractStatusAdmin(admin.ModelAdmin):
    search_fields = ('contract',)
    list_display = ['contract']
    list_filter = ['contract']


    def get_queryset(self, request):
        """
            Make sure to return appropriate queries :
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
