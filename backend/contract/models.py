from django.conf import settings
from django.db import models

from client.models import Client

employee_sales = settings.AUTH_USER_MODEL


# =================================================== CONTRACT MODEL


class Contract(models.Model):
    """
        Model representing a contract.
    """
    amount = models.FloatField(blank=True, null=True)
    payment_due = models.DateField(blank=True, null=True)
    status = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    # sales_contact = models.ForeignKey(
    #     employee_sales,
    #     on_delete=models.CASCADE,
    #     limit_choices_to={'role': 'sales'},
    #     null=True)

    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        null=False,
    )

    class Meta:
        ordering = ['-date_created']
        verbose_name = 'contract'
        verbose_name_plural = 'contracts'


    def __str__(self)-> str:
        """
            String for representing this Model object.
        """
        return f"Contract: {self.id} - Client: {self.client.company_name}"



class ContractManager(models.Model):
    contract = models.ForeignKey(
        Contract,
        on_delete=models.CASCADE,
        null=False
    )

    sales_contact = models.ForeignKey(
        employee_sales,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'sales'},
        null=True)

    # def __str__(self)-> str:
    #     """
    #         String for representing this Model object.
    #     """
    #     return f"Contract: {self.contract} Assignee: {self.sales_contact}"


class ContractStatus(models.Model):
    contract = models.OneToOneField(
        Contract,
        on_delete=models.CASCADE,
        null=False,
        primary_key=True
    )

    def __str__(self)-> str:
        """
            String for representing this Model object.
        """
        return f"Signed contract:  {self.contract.id}"
