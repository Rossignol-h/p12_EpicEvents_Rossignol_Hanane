from django.contrib import admin

from .models import Client


# ========================================================================


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):

    search_fields = ('company_name', 'email')
    list_display = ['upper_case_name', 'email', 'is_prospect', 'sales_contact']
    list_filter = ['is_prospect', 'sales_contact']
    readonly_fields = ['date_joined', 'date_updated', ]

    fieldsets = (
        ('Identity', {'fields': ('company_name', 'first_name', 'last_name')}),
        ('Contact', {'fields': ('email', 'phone', 'mobile')}),
        ('Employee in charge', {'fields': ('sales_contact',)}),
        ('Is he/she a prospect?', {'fields': ('is_prospect',)}),
    )

# ========================================================================

    def get_readonly_fields(self, request, obj=None):
        """
            Make sure to avoid a sales employee to change
            the sales_contact field, by adding it to readonly_fields
        """
        if request.user.role == 'sales':
            return self.readonly_fields + ['sales_contact', ]

        else:
            return self.readonly_fields

# ======================================================================== CUSOM COMPANY NAME DISPLAY

    @admin.display(description='Name')
    def upper_case_name(self, obj):
        return ("%s" % (obj.company_name)).upper()

# ======================================================================== OVERRIDE SAVE MODEL

    def save_model(self, request, obj, form, change):
        """
            If user is sales employee:
                Save him automatically
                as the sales_contact of this client.
            If user is superuser(manager), then the sales_contact
            is the one he choose.
        """
        if request.user.role == 'sales':
            obj.sales_contact = request.user
        elif request.user.is_superuser:
            obj.sales_contact = obj.sales_contact
        obj.save()

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
