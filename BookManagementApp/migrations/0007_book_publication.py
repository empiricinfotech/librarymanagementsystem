# Generated by Django 4.2 on 2023-04-26 13:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("BookManagementApp", "0006_alter_issuedbook_issued_date"),
    ]

    operations = [
        migrations.AddField(
            model_name="book",
            name="publication",
            field=models.CharField(default="aa", max_length=299),
            preserve_default=False,
        ),
    ]
