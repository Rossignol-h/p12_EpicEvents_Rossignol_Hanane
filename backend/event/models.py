from django.conf import settings
from django.db import models

from contract.models import ContractStatus
from authentication.models import Employee
from client.models import Client

employee_support = settings.AUTH_USER_MODEL


# =================================================== CUSTOM EVENT MODEL


class Event(models.Model):
    """
        Model representing an event.
    """
    name = models.CharField(max_length=50, blank=False, null=False, unique=True)
    attendees = models.PositiveIntegerField(blank=True, null=True)
    notes = models.TextField(max_length=1000, blank=True, null=True)
    event_date = models.DateField(blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    event_status = models.ForeignKey(
        ContractStatus,
        related_name="event",
        on_delete=models.CASCADE,
        null=True
    )

    client = models.ForeignKey(
        Client,
        related_name="event_client",
        on_delete=models.CASCADE,
        null=True
    )

    support_contact = models.ForeignKey(
        Employee,
        default=1,
        on_delete=models.SET_DEFAULT,
        limit_choices_to={'role': 'support'},
        null=True
    )

    class Meta:
        ordering = ['-date_updated']
        verbose_name = 'event'
        verbose_name_plural = 'events'
        constraints = [models.UniqueConstraint(fields=['event_status', 'name'], name="unique_event")]

    def __str__(self):
        """
            String representing this Model object.
        """
        return f"Event : {self.name}"
