# Generated by Django 5.1.2 on 2024-11-22 11:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("authentication", "0005_alter_user_phone"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="user",
            name="organization_name",
        ),
    ]
