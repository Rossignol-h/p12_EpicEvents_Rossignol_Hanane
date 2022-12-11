# Generated by Django 4.1.3 on 2022-12-11 12:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('client', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='is_prospect',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='client',
            name='sales_contact',
            field=models.ForeignKey(limit_choices_to={'role': 'sales'}, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]
