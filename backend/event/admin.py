from django.contrib import admin
from django import forms

from .models import Event


# ======================================================== CUSTOM MODEL FORM


class EventAdminForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = '__all__'

    # def save(self, commit=True):
    #     """
    #         Automatically add the client of the contract
    #         to the event, then save it.
    #     """
    #     event = super().save(commit=False)
    #     event.client = event.event_status.contract.client
    #     if commit:
    #         event.save()
    #     return event


# ======================================================== CUSTOM ADMIN PAGE


class EventAdmin(admin.ModelAdmin):
    '''
    Add the custom form
    customize all the fields in the admin
    '''
    form = EventAdminForm
    search_fields = ['event_date']
    list_display = ['name', 'attendees', 'event_date', 'client', 'support_contact']
    list_filter = ['client', 'event_date']
    readonly_fields = ('date_created', 'date_updated', 'event_status', 'client')

    fieldsets = (
        ('Contract related', {'fields': ('event_status',)}),
        ('Client related', {'fields': ('client',)}),
        ('Date', {'fields': ('event_date','date_created', 'date_updated')}),
        ('Details', {'fields': ('name','attendees', 'notes')}),
        ('Employee in charge', {'fields': ('support_contact',)}),
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(support_contact=request.user)

    def get_client_email(self, obj):
        return obj.client.email

    @admin.display(empty_value='???')
    def support_contact(self, obj):
        return obj.support_contact

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
