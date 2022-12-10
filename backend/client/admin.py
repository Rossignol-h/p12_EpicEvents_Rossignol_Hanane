from django.contrib import admin

from event.models import Event
from .models import Client


# ========================================================================


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):

    search_fields = ('company_name', 'email')
    list_display = ['company_name', 'email', 'is_prospect','sales_contact']
    list_filter = ['is_prospect', 'sales_contact']
    readonly_fields = ['date_joined', 'date_updated',]

    fieldsets = (
        ('Identity',{'fields': ('company_name', 'first_name', 'last_name')}),
        ('Contact', {'fields': ('email', 'phone', 'mobile')}),
        ('Employee in charge', {'fields': ('sales_contact',)}),
        ('Is he/she a prospect?', {'fields': ('is_prospect',)}),
    )

# ========================================================================

    def get_queryset(self, request):
        """
            Make sure to return appropriate queries :
            if the user is superuser(manager) ==> return all clients
            if the user role is sales ==> return only clients, that he is in charge of 
            if the user is support ==> return only clients of events, that he is in charge of
        """

        queryset = super().get_queryset(request)
        employee = request.user

        if employee.role == 'sales':
            return Client.objects.filter(sales_contact=employee)
            
        if employee.role == 'support':
            clients = [e.client.id for e in Event.objects.filter(support_contact=employee)]
            for client in clients:
                return Client.objects.filter(id=client)

        elif employee.is_superuser:
            return Client.objects.all()

        else:
            return queryset.none()

# ========================================================================

    def get_readonly_fields(self, request, obj=None):
        """
            Make sure to avoid a sales employee to change 
            the sales_contact field, by adding it to readonly_fields 
        """

        if request.user.role == 'sales':
            return self.readonly_fields + ['sales_contact',]
        else:
            return self.readonly_fields

# ========================================================================

    def save_model(self, request, obj, form, change):
        """
            Save automatically the current sales employee
            as the sales_contact of this client.
        """

        obj.sales_contact = request.user
        obj.save()
