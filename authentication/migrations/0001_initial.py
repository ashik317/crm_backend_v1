# Generated by Django 5.1.2 on 2024-11-07 11:50

import common.fields
import django.db.models.deletion
import enumerify.fields
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="User",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("password", models.CharField(max_length=128, verbose_name="password")),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                (
                    "is_superuser",
                    models.BooleanField(
                        default=False,
                        help_text="Designates that this user has all permissions without explicitly assigning them.",
                        verbose_name="superuser status",
                    ),
                ),
                (
                    "alias",
                    models.UUIDField(
                        db_index=True, default=uuid.uuid4, editable=False, unique=True
                    ),
                ),
                (
                    "status",
                    enumerify.fields.SelectIntegerField(
                        choices=[
                            (0, "Active"),
                            (1, "Inactive"),
                            (2, "Draft"),
                            (3, "Released"),
                            (4, "Approved Draft"),
                            (5, "Absent"),
                            (6, "Purchase Order"),
                            (7, "Suspend"),
                            (8, "On Hold"),
                            (9, "Hardwired"),
                            (10, "Loss"),
                            (11, "Freeze"),
                            (12, "For Adjustment"),
                            (13, "Distributor Order"),
                        ],
                        default=0,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "user_ip",
                    models.GenericIPAddressField(blank=True, editable=False, null=True),
                ),
                (
                    "email",
                    models.EmailField(
                        db_index=True, default=None, max_length=254, unique=True
                    ),
                ),
                (
                    "phone",
                    models.CharField(
                        db_index=True, default=None, max_length=24, null=True
                    ),
                ),
                ("first_name", models.CharField(blank=True, max_length=64)),
                ("last_name", models.CharField(blank=True, max_length=64)),
                (
                    "profile_image",
                    common.fields.TimestampThumbnailImageField(
                        blank=True, null=True, upload_to="user/profile"
                    ),
                ),
                (
                    "nid",
                    models.CharField(
                        blank=True,
                        default=None,
                        help_text="National ID No. Example: YYYYXXXXXXXXXXXXX",
                        max_length=64,
                        null=True,
                        unique=True,
                        verbose_name="NID No.",
                    ),
                ),
                (
                    "is_staff",
                    models.BooleanField(
                        default=False,
                        help_text="Designates whether the user can log into this admin site.",
                        verbose_name="staff status",
                    ),
                ),
                (
                    "is_active",
                    models.BooleanField(
                        default=True,
                        help_text="Designates whether this user should be treated as active.",
                        verbose_name="active",
                    ),
                ),
                (
                    "user_type",
                    models.CharField(
                        choices=[
                            (1, "Lead"),
                            (2, "Client"),
                            (3, "Introducer"),
                            (4, "Service Holder"),
                        ],
                        default=1,
                        max_length=20,
                    ),
                ),
                (
                    "city",
                    models.CharField(
                        blank=True,
                        db_index=True,
                        default=None,
                        max_length=64,
                        null=True,
                    ),
                ),
                (
                    "state",
                    models.CharField(
                        blank=True,
                        db_index=True,
                        default=None,
                        max_length=64,
                        null=True,
                    ),
                ),
                (
                    "country",
                    models.CharField(
                        blank=True,
                        db_index=True,
                        default=None,
                        max_length=64,
                        null=True,
                    ),
                ),
                (
                    "zip_code",
                    models.CharField(
                        blank=True,
                        db_index=True,
                        default=None,
                        max_length=64,
                        null=True,
                    ),
                ),
                (
                    "address",
                    models.CharField(
                        blank=True,
                        db_index=True,
                        default=None,
                        max_length=255,
                        null=True,
                    ),
                ),
                (
                    "created_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="created_%(class)s_set",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Created By",
                    ),
                ),
                (
                    "groups",
                    models.ManyToManyField(
                        blank=True, related_name="organization_groups", to="auth.group"
                    ),
                ),
                (
                    "updated_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="updated_%(class)s_set",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Updated By",
                    ),
                ),
                (
                    "user_permissions",
                    models.ManyToManyField(
                        blank=True,
                        related_name="organization_user_permissions",
                        to="auth.permission",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
