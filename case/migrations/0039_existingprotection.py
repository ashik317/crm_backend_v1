# Generated by Django 5.1.2 on 2025-03-10 08:12

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("case", "0038_solicitoraccountant_name"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="ExistingProtection",
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
                (
                    "alias",
                    models.UUIDField(
                        db_index=True, default=uuid.uuid4, editable=False, unique=True
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "user_ip",
                    models.GenericIPAddressField(blank=True, editable=False, null=True),
                ),
                (
                    "have_any_existing_Protection_policies_in_place",
                    models.BooleanField(default=False),
                ),
                (
                    "policy_type",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("MORTGAGE", "Mortgage"),
                            ("PROTECTION", "Protection"),
                            ("GENERAL_INSURANCE", "General Insurance"),
                        ],
                        max_length=255,
                        null=True,
                    ),
                ),
                ("policy_provider", models.CharField(max_length=255)),
                (
                    "insurers_reference",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "sum_assured",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=12, null=True
                    ),
                ),
                ("premium", models.DecimalField(decimal_places=2, max_digits=12)),
                (
                    "premium_payment_type",
                    models.CharField(
                        blank=True,
                        choices=[("MONTHLY", "Monthly"), ("ANNUALLY", "Annually")],
                        max_length=255,
                        null=True,
                    ),
                ),
                ("person_assured", models.CharField(max_length=255)),
                (
                    "in_trust",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("NA", "N/A"),
                            ("YES", "Yes"),
                            ("NO", "NO"),
                            ("CLIENT_TO_ASCERTAIN", "Client To Ascertain"),
                        ],
                        max_length=255,
                        null=True,
                    ),
                ),
                (
                    "guaranteed_reviewable",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("NA", "N/A"),
                            ("GUARANTEED", "Guaranteed"),
                            ("REVIEWABLE", "Reviewable"),
                            ("CLIENT_TO_ASCERTAIN_AGE", "Client To Ascertain"),
                            ("COSTED", "Costed"),
                        ],
                        max_length=255,
                        null=True,
                    ),
                ),
                ("remaining_policy_term", models.CharField(max_length=255)),
                ("cancelled_lapsed_date", models.DateField()),
                ("renewal_date", models.DateField()),
                ("date_policy_started", models.DateField()),
                ("waiver_of_premium", models.BooleanField(default=False)),
                ("indexation", models.BooleanField(default=False)),
                ("death_in_service_provision", models.BooleanField(default=False)),
                (
                    "have_non_standard_terms_been_issued",
                    models.BooleanField(default=False),
                ),
                (
                    "copy_and_paste_non_standard_terms_from_lender",
                    models.TextField(blank=True, null=True),
                ),
                ("will_this_policy_be_cancelled", models.BooleanField(default=False)),
                (
                    "reason_for_policy_cancellation",
                    models.CharField(
                        blank=True,
                        choices=[("NOT_VALUES_YET", "Not Values Yet")],
                        max_length=255,
                        null=True,
                    ),
                ),
                ("policy_cancellation_notes", models.TextField(blank=True, null=True)),
                (
                    "why_did_you_take_out_this_policy",
                    models.TextField(blank=True, null=True),
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
            ],
            options={
                "ordering": ("-created_at", "-updated_at"),
            },
        ),
    ]
