# Generated by Django 5.1.2 on 2025-03-08 06:18

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "case",
            "0035_adverse_have_you_ever_entered_into_an_individual_voluntary_arrangement",
        ),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Property",
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
                ("is_property_owner", models.BooleanField(default=False)),
                ("postcode", models.CharField(max_length=255)),
                ("house_name_or_number", models.CharField(max_length=255)),
                ("address_1", models.CharField(max_length=255)),
                ("address_2", models.CharField(blank=True, max_length=255, null=True)),
                ("city", models.CharField(max_length=255)),
                ("county", models.CharField(blank=True, max_length=255, null=True)),
                ("country", models.CharField(max_length=255)),
                (
                    "property_value",
                    models.DecimalField(decimal_places=2, max_digits=12),
                ),
                (
                    "current_mortgage_balance",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=12, null=True
                    ),
                ),
                (
                    "monthly_rental_income",
                    models.DecimalField(decimal_places=2, max_digits=12),
                ),
                (
                    "monthly_mortgage_payment",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=12, null=True
                    ),
                ),
                (
                    "value_at_purchase",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=12, null=True
                    ),
                ),
                ("date_purchased", models.DateField(blank=True, null=True)),
                ("is_hmo", models.BooleanField(default=False)),
                ("is_mufb", models.BooleanField(default=False)),
                (
                    "mortgage_lender",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "repayment_type",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "to_be_repaid",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=12, null=True
                    ),
                ),
                (
                    "current_rate",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=5, null=True
                    ),
                ),
                (
                    "rate_type",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("unknown", "Unknown"),
                            ("fixed", "Fixed"),
                            ("variable", "Variable"),
                            ("tracker", "Tracker"),
                            ("libor_linked", "Libor Linked"),
                            ("discount", "Discount"),
                            ("capped", "Capped"),
                            ("all", "All"),
                            ("svr", "SVR"),
                            ("offset", "Offset"),
                            ("lifetime", "Lifetime"),
                            ("other", "Other"),
                        ],
                        max_length=255,
                        null=True,
                    ),
                ),
                ("current_rate_end_date", models.DateField(blank=True, null=True)),
                ("erc_end_date", models.DateField(blank=True, null=True)),
                (
                    "account_number",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                ("property_type", models.CharField(max_length=255)),
                ("ownership", models.CharField(max_length=255)),
                ("leasehold", models.IntegerField(blank=True, null=True)),
                ("year_built", models.IntegerField(blank=True, null=True)),
                ("number_of_bedrooms", models.IntegerField()),
                ("remaining_mortgage_term", models.IntegerField(blank=True, null=True)),
                ("is_limited_company", models.BooleanField(default=False)),
                (
                    "epc_rating",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("unknown", "Unknown"),
                            ("a", "A"),
                            ("b", "B"),
                            ("c", "C"),
                            ("d", "D"),
                            ("e", "E"),
                            ("f", "F"),
                            ("g", "G"),
                        ],
                        max_length=255,
                        null=True,
                    ),
                ),
                (
                    "applicant",
                    models.ManyToManyField(
                        related_name="applicant_property", to=settings.AUTH_USER_MODEL
                    ),
                ),
                (
                    "case",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="property",
                        to="case.case",
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
