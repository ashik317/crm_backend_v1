# Generated by Django 5.1.2 on 2025-02-19 05:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("case", "0016_alter_applicantdetails_case"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="applicantdetails",
            options={
                "ordering": ["-created_at", "-updated_at"],
                "verbose_name": "Applicant Detail",
                "verbose_name_plural": "Applicant Details",
            },
        ),
        migrations.AlterModelOptions(
            name="loandetails",
            options={
                "ordering": ["-created_at", "-updated_at"],
                "verbose_name": "Loan Detail",
                "verbose_name_plural": "Loan Details",
            },
        ),
    ]
