from django.contrib import admin

from .models import Event
from contract.models import ContractStatus


# ======================================================== CUSTOM ADMIN PAGE

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    '''
    Add the custom form
    customize all the fields in the admin
    '''
    empty_value_display = 'will be automatically added'
    search_fields = ['event_date']
    list_display = ['name', 'attendees', 'event_date', 'client', 'support_contact']
    list_filter = ['client', 'event_date']
    readonly_fields = ('date_created', 'date_updated', 'client')

    fieldsets = (
        ('Contract related', {'fields': ('event_status',)}),
        ('Client related', {'fields': ('client',)}),
        ('Date', {'fields': ('event_date', 'date_created', 'date_updated')}),
        ('Details', {'fields': ('name', 'attendees', 'notes')}),
        ('Employee in charge', {'fields': ('support_contact',)}),
    )

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
            return self.readonly_fields + ['sales_contact', 'client', ]
        # 'add' form
        if obj is None and request.user.role == 'sales':
            return self.readonly_fields + ('support_contact',)

        else:
            return self.readonly_fields

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
            if db_field.name == "event_status":
                kwargs["queryset"] = ContractStatus.objects.filter(contract__sales_contact=request.user)

        if request.user.is_superuser:
            if db_field.name == "event_status":
                kwargs["queryset"] = ContractStatus.objects.all()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def get_client_email(self, obj):
        return obj.client.email

# ======================================================== RESTRICT PERMISSION

    def has_change_permission(self, request, obj=None):
        """
            Only the support employee in charge of the current event,
            or manager
            can update it.
        """
        if request.user.role == 'support':
            if obj is not None and obj.support_contact == request.user:
                return True
        elif request.user.is_superuser:
            return True
        else:
            return False

# ========================================================================

    def save_model(self, request, obj, form, change):
        """

        """
        obj.client = obj.event_status_contract.client
        obj.save()
