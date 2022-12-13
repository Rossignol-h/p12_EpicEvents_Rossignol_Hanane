from phonenumber_field.modelfields import PhoneNumberField
from django.conf import settings
from django.db import models

employee_sales = settings.AUTH_USER_MODEL


# =================================================== CLIENT MODEL


class Client(models.Model):
    """
        Model representing a prospect or a client.
    """

    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    email = models.EmailField(max_length=100, unique=True)
    phone = PhoneNumberField(blank=False, unique=True)
    mobile = PhoneNumberField(blank=False, unique=True)
    company_name = models.CharField(blank=False, max_length=50, unique=True)
    is_prospect = models.BooleanField(blank=False, default=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    sales_contact = models.ForeignKey(
        employee_sales,
        default=1,
        on_delete=models.SET_DEFAULT,
        limit_choices_to={'role': 'sales'},
        blank=False,
        null=False)

    class Meta:
        ordering = ['-is_prospect']
        verbose_name = 'client'
        verbose_name_plural = 'clients'

    def __str__(self) -> str:
        """
            String representing this Model object.
        """
        return f"{self.company_name}"
