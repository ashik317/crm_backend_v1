# Generated by Django 5.1.2 on 2024-11-08 14:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("organization", "0004_remove_organization_status_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="organization",
            name="contact_person_designation",
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
    ]
