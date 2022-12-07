from django.contrib import admin
from .models import Event
from django import forms


# ======================================================== CUSTOM MODEL FORM


class EventAdminForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = '__all__'

    def save(self, commit=True):
        """
            Automatically add the client of the contract
            to the event, then save it.
        """
        event = super().save(commit=False)
        event.client = event.event_status.contract.client
        if commit:
            event.save()
        return event

# ======================================================== CUSTOM ADMIN PAGE


class EventAdmin(admin.ModelAdmin):
    '''
    Add the custom form
    customize all the fields in the admin
    '''
    form = EventAdminForm
    search_fields = ['event_date', 'client_id__email', 'client_id__company_name']
    list_display = ['name', 'attendees', 'event_date', 'client_id', 'support_contact']
    list_filter = ['client_id', 'event_date']
    readonly_fields = ('date_created', 'date_updated','support_contact')

    fieldsets = (
        ('Contract related', {'fields': ('event_status',)}),
        ('Date', {'fields': ('event_date','date_created', 'date_updated')}),
        ('Details', {'fields': ('name','attendees', 'notes')}),
        ('Contact', {'fields': ('support_contact',)}),
    )

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

admin.site.register(Event, EventAdmin)
