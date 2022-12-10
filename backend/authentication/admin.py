from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
from django import forms

from .models import Employee

# ======================================================== CUSTOM MODEL FORM


class EmployeeAdminForm(forms.ModelForm):
    """
        Form for creating new employees. Includes all the required
        fields, & repeated password.
    """
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)
    
    class Meta:
        model = Employee
        fields = '__all__'

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def clean_email(self):
        """
            Make sure that the email address 
            ends with epicevents.com, 
            for avoiding enter personnal employee's email.
        """
        email = self.cleaned_data["email"]
        if not email.endswith('@epicevents.com'):
            raise forms.ValidationError("Please, email has to end with epicevents.com")
        return self.cleaned_data["email"]

    def save(self, commit=True):
        """
            Make sure that the password is hashed
            before saving an employee.
        """
        user = super(EmployeeAdminForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

# ======================================================== CUSTOM USER ADMIN


@admin.register(Employee)
class EmployeeAdmin(UserAdmin):

    add_form = EmployeeAdminForm
    search_fields = ('email',)
    list_display = ['email', 'role', 'phone_number', 'is_superuser']
    list_filter = ['role',]

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2','phone_number' , 'role' ),
        }),
    )

    fieldsets = (
        (None, {'fields': ('email',)}),
        ('Contact', {'fields': ('phone_number',)}),
        ('Security', {'fields': ('password',)}),
        ('Permissions', {'fields': ('role',)}),
    )

    radio_fields = {'role': admin.HORIZONTAL}
    ordering = ('id',)
