# Generated by Django 5.1.2 on 2025-02-10 06:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("case", "0011_loandetails"),
    ]

    operations = [
        migrations.RenameField(
            model_name="loandetails",
            old_name="deposit_amount",
            new_name="current_monthly_payment",
        ),
        migrations.RenameField(
            model_name="loandetails",
            old_name="purchase_price",
            new_name="property_valuation",
        ),
        migrations.RemoveField(
            model_name="loandetails",
            name="deposit_source",
        ),
        migrations.RemoveField(
            model_name="loandetails",
            name="introducer",
        ),
        migrations.AddField(
            model_name="loandetails",
            name="current_lender",
            field=models.CharField(
                blank=True,
                choices=[
                    ("UNKNOWN", "Unknown"),
                    ("ACCORD_MORTGAGES", "Accord Mortgages"),
                    ("AHLI_UNITED_BANK", "Ahli United Bank"),
                    ("AL_RAYAN_BANK", "Al Rayan Bank"),
                    ("ALDERMORE_MORTGAGES", "Aldermore Mortgages"),
                    ("AMICUS_PLC", "Amicus PLC"),
                    ("ASSETZ_CAPITAL", "Assetz Capital"),
                    ("ATOM_BANK", "Atom Bank"),
                    ("AVIVA_EQUITY_RELEASE", "Aviva Equity Release"),
                    ("AXIS_BANK", "Axis Bank"),
                    ("BANK_AND_CLIENTS_PLC", "Bank & Clients PLC"),
                    ("BANK_OF_CHINA", "Bank of China"),
                    ("BANK_OF_CYPRUS_UK", "Bank of Cyprus UK"),
                    ("BANK_OF_IRELAND", "Bank of Ireland"),
                    ("BARCLAYS", "Barclays"),
                    ("BARCLAYS_COMMERCIAL", "Barclays Commercial"),
                    ("BATH_BUILDING_SOCIETY", "Bath Building Society"),
                    ("BEVERLEY_BUILDING_SOCIETY", "Beverley Building Society"),
                    ("BLUESTONE_MORTGAGES", "Bluestone Mortgages"),
                    ("BLUEZEST", "BlueZest"),
                    ("BM_SOLUTIONS", "BM Solutions"),
                    ("BOOST_CAPITAL", "Boost Capital"),
                    ("BRIDGEWATER_EQUITY_RELEASE", "Bridgewater Equity Release"),
                    (
                        "BUCKINGHAMSHIRE_BUILDING_SOCIETY",
                        "Buckinghamshire Building Society",
                    ),
                    ("CAMBRIDGE_AND_COUNTIES_BANK", "Cambridge and Counties Bank"),
                    ("CAMBRIDGE_BUILDING_SOCIETY", "Cambridge Building Society"),
                    ("CENTRAL_TRUST", "Central Trust"),
                    ("CHARTERBANK", "Charterbank"),
                    ("CHL_MORTGAGES", "CHL Mortgages"),
                    (
                        "CHORLEY_AND_DISTRICT_BUILDING_SOCIETY",
                        "Chorley & District Building Society",
                    ),
                    ("CLEARLY_LOANS", "Clearly Loans"),
                    ("CLYDESDALE_BANK", "Clydesdale Bank"),
                    ("COUTTS", "Coutts"),
                    ("COVENTRY_BUILDING_SOCIETY", "Coventry Building Society"),
                    ("CROWN_EQUITY_RELEASE", "Crown Equity Release"),
                    ("CUMBERLAND_BUILDING_SOCIETY", "Cumberland Building Society"),
                    ("DANSKE_BANK", "Danske Bank"),
                    ("DARLINGTON_BUILDING_SOCIETY", "Darlington Building Society"),
                    ("DIGITAL_MORTGAGES", "Digital Mortgages"),
                    ("DUDLEY_BUILDING_SOCIETY", "Dudley Building Society"),
                    ("EARL_SHILTON_BUILDING_SOCIETY", "Earl Shilton Building Society"),
                    ("ECOLOGY_BUILDING_SOCIETY", "Ecology Building Society"),
                    ("EQUIFINANCE", "Equifinance"),
                    ("FAMILY_BUILDING_SOCIETY", "Family Building Society"),
                    ("FINSEC", "FinSec"),
                    ("FIRST_TRUST_BANK", "First Trust Bank"),
                    ("UNKNOWN_DEFAULT", "Unknown (Default)"),
                ],
                max_length=50,
                null=True,
            ),
        ),
        migrations.AddField(
            model_name="loandetails",
            name="date_of_purchase",
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="loandetails",
            name="original_purchase_price",
            field=models.DecimalField(
                blank=True, decimal_places=2, default=0.0, max_digits=15, null=True
            ),
        ),
        migrations.AddField(
            model_name="loandetails",
            name="outstanding_balance",
            field=models.DecimalField(
                blank=True, decimal_places=2, max_digits=15, null=True
            ),
        ),
    ]
