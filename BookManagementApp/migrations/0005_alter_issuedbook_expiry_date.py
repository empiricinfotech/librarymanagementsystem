# Generated by Django 4.2 on 2023-04-26 05:00

import BookManagementApp.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "BookManagementApp",
            "0004_alter_issuedbook_options_issuedbook_requested_date_and_more",
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name="issuedbook",
            name="expiry_date",
            field=models.DateField(default=BookManagementApp.models.expiry, null=True),
        ),
    ]
