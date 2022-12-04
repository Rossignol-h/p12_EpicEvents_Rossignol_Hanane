from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser
from permissions import add_to_group
from django.db import models


# ============================================= CUSTOM MODEL MANAGER


class CustomUserManager(BaseUserManager):
    """
        Custom user model manager where email is the unique identifiers
        for authentication instead of usernames.
    """
    def create_user(self, email, password, **extra_fields):
        """
            Create and save a User with the given email and password.
        """
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        add_to_group(user)
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
            Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)


# =================================================== EMPLOYEE MODEL


class Employee(AbstractUser):
    """
        Model representing an employee.
    """

    ROLES_CHOICES = [('sales', 'sales'),('support', 'support')]

    username = None
    email = models.EmailField(blank=False, unique=True)
    phone_number = PhoneNumberField(blank=False, unique=True)
    role = models.CharField(blank=False, null= False, max_length=10, choices=ROLES_CHOICES)
    is_staff = models.BooleanField(default=True, editable=False)
    is_superuser = models.BooleanField(default=False, editable=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self)-> str:
        """
            String representing this Model object.
        """
        return f"{self.email}"
