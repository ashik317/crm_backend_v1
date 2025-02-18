# Generated by Django 5.1.2 on 2025-02-18 09:48

import django_countries.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("case", "0014_companyinfo_applicantdetails_dependant_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="applicantdetails",
            name="mortgage_account_number",
            field=models.CharField(blank=True, max_length=50, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name="applicantdetails",
            name="nationality",
            field=django_countries.fields.CountryField(
                blank=True, max_length=2, null=True
            ),
        ),
    ]
