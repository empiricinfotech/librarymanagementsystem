# Generated by Django 4.2 on 2023-04-19 05:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("BookManagementApp", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="book",
            name="bookNo",
            field=models.IntegerField(unique=True),
        ),
    ]
