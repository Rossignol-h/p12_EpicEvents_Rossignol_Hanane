from django.conf import settings
from django.db import models

from client.models import Client

employee_sales = settings.AUTH_USER_MODEL


# ======================================================================== CONTRACT MODEL


class Contract(models.Model):
    """
        Model representing a contract 
        create by a sales employee.
    """
    amount = models.FloatField(blank=True, null=True)
    payment_due = models.DateField(blank=True, null=True)
    status = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    client = models.ForeignKey(
        Client,
        related_name="client_contract",
        on_delete=models.CASCADE,
        null=True
    )

    sales_contact = models.ForeignKey(
        employee_sales,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'sales'},
        null=True)

    class Meta:
        ordering = ['-date_created']
        verbose_name = 'contract'
        verbose_name_plural = 'contracts'

    def __str__(self):
        """
            String for representing this Model object.
        """
        return f"Contract: {self.id} - Client: {self.client.company_name}  - Sales contact: {self.sales_contact}"


# ======================================================================== SIGNED CONTRACTS MODELS


class ContractStatus(models.Model):
    """
        Model representing a signed contract, 
        then an event can be create.
    """
    contract = models.OneToOneField(
        Contract,
        on_delete=models.DO_NOTHING,
        limit_choices_to={'status': 'True'},
        null=False,
        primary_key=True
    )
