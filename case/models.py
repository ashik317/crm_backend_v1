from django.db import models
from django.db.models.functions import Lead
from django.db.models.signals import post_save
from django_countries.fields import CountryField
from django_filters.fields import ChoiceField
from multiselectfield import MultiSelectField

from authentication.models import User
from common.models import CreatedAtUpdatedAtBaseModel
from common.enums import (
    ProductCategoryChoices,
    ApplicantTypeChoices,
    CaseStageChoices,
    CaseStatusChoices,
    FileTypeChoices,
    MeetingTypeChoices,
    MeetingStatusChoices,
)
from organization.models import Organization
from .enums import (
    ApplicationTypeChoices,
    MortgageTypeChoices,
    LoanPurposeChoices,
    LenderChoices,
    BorrowerTypeChoices,
    RepaymentMethodChoices,
    RepaymentVehicleChoices,
    InterestRateTypeChoices,
    ProductTermChoices,
    AdviceLevelChoices,
    IntroductionTypeChoices,
    IntroducerPaymentTermsChoices,
    LeadSourceChoices,
    SaleTypeChoices,
    CurrentLenderChoices,
    TitleChoices,
    GenderChoices,
    MaritalStatusChoices,
    MarketingPreferencesChoices,
    ResidentialStatus,
    MortgageType,
    RepaymentType,
    InterestType,
    ERCCompletionStatus,
    PropertyType,
    TenureType,
    RoleType,
    CompanyType,
    EmploymentStatus,
    EmploymentType,
    FrequencyChoice,
    RateTypeChoices,
    EPCRatingChoices,
    UserTypeChoices,
    PremiumPaymentChoices,
    InTrustChoices, GuaranteedReviewableChoices, PolicyCancellationChoices,
)
from .signals import (
    create_loan_details,
    create_applicant_details,
    create_applicant_details_for_joint_user,
    create_employment_details_for_lead,
    create_employment_details_for_joint_user,
    create_adverse_for_lead,
    create_adverse_for_joint_user,
)
from .utils import upload_to_case_files


class Case(CreatedAtUpdatedAtBaseModel):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    lead = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, blank=True)
    case_category = models.CharField(
        max_length=50,
        choices=ProductCategoryChoices.choices,
        default=ProductCategoryChoices.MORTGAGE,
        db_index=True,
    )
    applicant_type = models.CharField(
        max_length=50,
        choices=ApplicantTypeChoices.choices,
        default=ApplicantTypeChoices.SINGLE,
        db_index=True,
    )
    case_status = models.CharField(
        max_length=50,
        choices=CaseStatusChoices.choices,
        default=CaseStatusChoices.NEW_LEAD,
        db_index=True,
    )
    case_stage = models.CharField(
        max_length=50,
        choices=CaseStageChoices.choices,
        default=CaseStageChoices.INQUIRY,
        db_index=True,
    )
    notes = models.TextField(blank=True, null=True)
    is_removed = models.BooleanField(default=False, blank=True, db_index=True)

    class Meta:
        ordering = ["-created_at", "-updated_at"]

    def __str__(self):
        return self.name

    def generate_case_name(self):
        # Mapping case stage choices to abbreviations
        stage_mapping = {
            "INQUIRY": "INQ",
            "FACT_FIND": "FFD",
            "RESEARCH_COMPLIANCE_CHECK": "RCC",
            "DECISION_IN_PRINCIPLE": "DIP",
            "FULL_MORTGAGE_APPLICATION": "FMA",
            "OFFER_FROM_BANK": "OFB",
            "LEGAL": "LEG",
            "COMPLETION": "COM",
            "FUTURE_OPPORTUNITY": "FOP",
            "NOT_PROCEED": "NPD",
        }
        # Get the 3-letter abbreviation for the case stage
        stage_abbreviation = stage_mapping.get(self.case_stage, "UNK")
        # Use the last 8 characters of the alias
        alias_suffix = str(self.alias).replace("-", "")[-8:]
        return f"{stage_abbreviation}-{alias_suffix}"

    def save(self, *args, **kwargs):
        # Check if the case_stage has changed
        if self.pk:  # Check if the instance already exists (for updates)
            original = Case.objects.get(pk=self.pk)
            if original.case_stage != self.case_stage:
                # If the case_stage is different, regenerate the name
                self.name = self.generate_case_name()
        else:
            # For new cases, generate the name if not set
            if not self.name:
                self.name = self.generate_case_name()

        # Call the parent save method
        super().save(*args, **kwargs)


class Files(CreatedAtUpdatedAtBaseModel):
    case = models.ForeignKey(
        Case,
        on_delete=models.CASCADE,
        related_name="files",
        verbose_name="Related Case",
    )
    file = models.FileField(
        upload_to=upload_to_case_files,
        verbose_name="File",
        help_text="Upload the file",
    )
    file_type = models.CharField(
        max_length=50,
        choices=FileTypeChoices.choices,
        default=FileTypeChoices.IDS,
        db_index=True,
    )
    file_owner = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True, db_index=True
    )
    is_removed = models.BooleanField(default=False, db_index=True)
    name = models.CharField(
        max_length=500,
        blank=True,
        null=True,
        verbose_name="File Name",
        help_text="Optional name of the file",
    )
    description = models.CharField(
        max_length=1000,
        blank=True,
        null=True,
        verbose_name="Description",
        help_text="Optional description of the file",
    )
    special_notes = models.CharField(
        max_length=1000,
        blank=True,
        null=True,
        verbose_name="Special Notes",
        help_text="Optional special notes related to the file",
    )

    class Meta:
        ordering = ["-created_at", "-updated_at"]
        verbose_name = "Case File"
        verbose_name_plural = "Case Files"

    def __str__(self):
        return f"{self.case.name} - {self.file.name}"


class JointUser(CreatedAtUpdatedAtBaseModel):
    case = models.ForeignKey(
        Case,
        on_delete=models.CASCADE,
        related_name="joint_users",
        verbose_name="Related Case",
    )
    joint_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="joint_user_cases",
        verbose_name="Joint User",
    )
    relationship = models.CharField(
        max_length=100,
        blank=True,
        null=True,
    )
    notes = models.TextField(
        blank=True,
        null=True,
        verbose_name="Notes",
        help_text="Additional notes about the joint user",
    )
    is_removed = models.BooleanField(default=False, db_index=True)

    class Meta:
        ordering = ["-created_at", "-updated_at"]
        verbose_name = "Joint User"
        verbose_name_plural = "Joint Users"

    def __str__(self):
        return f"(Case: {self.case.name}) Joint User: {self.joint_user}"


class Meeting(CreatedAtUpdatedAtBaseModel):
    case = models.ForeignKey(
        Case,
        on_delete=models.CASCADE,
        related_name="meetings",
        verbose_name="Related Case",
    )
    meeting_type = models.CharField(
        max_length=50,
        choices=MeetingTypeChoices.choices,
        default=MeetingTypeChoices.UPCOMING,
        db_index=True,
    )
    meeting_status = models.CharField(
        max_length=50,
        choices=MeetingStatusChoices.choices,
        default=MeetingStatusChoices.CONFIRMED,
        db_index=True,
    )
    special_notes = models.CharField(max_length=500, null=True, blank=True)
    meeting_link = models.URLField(null=True, blank=True)
    meeting_date = models.DateField(null=True, blank=True)
    meeting_time = models.TimeField(null=True, blank=True)
    is_removed = models.BooleanField(default=False, db_index=True)

    class Meta:
        ordering = ["-created_at", "-updated_at"]
        verbose_name = "Meeting"


class LoanDetails(CreatedAtUpdatedAtBaseModel):
    case = models.OneToOneField(
        Case,
        on_delete=models.CASCADE,
        related_name="loan_details",
        verbose_name="Related Case",
    )
    application_type = models.CharField(
        max_length=50,
        choices=ApplicationTypeChoices.choices,
        default=ApplicationTypeChoices.SELECT_APPLICATION_TYPE,
    )

    mortgage_type = models.CharField(
        max_length=50, choices=MortgageTypeChoices.choices, blank=True, null=True
    )
    loan_purpose = models.CharField(
        max_length=50, choices=LoanPurposeChoices.choices, blank=True, null=True
    )
    lender = models.CharField(
        max_length=50, choices=LenderChoices.choices, blank=True, null=True
    )
    lenders_reference = models.CharField(max_length=100, blank=True, null=True)
    borrower_type = models.CharField(
        max_length=50, choices=BorrowerTypeChoices.choices, blank=True, null=True
    )
    repayment_method = models.CharField(
        max_length=50, choices=RepaymentMethodChoices.choices, blank=True, null=True
    )
    repayment_vehicle = models.CharField(
        max_length=50, choices=RepaymentVehicleChoices.choices, blank=True, null=True
    )
    interest_rate_type = models.CharField(
        max_length=50, choices=InterestRateTypeChoices.choices, blank=True, null=True
    )
    product_term = models.CharField(
        max_length=50, choices=ProductTermChoices.choices, blank=True, null=True
    )
    property_valuation = models.PositiveIntegerField(default=0)
    purchase_price = models.PositiveIntegerField(default=0)
    loan_amount = models.PositiveIntegerField(default=0)
    estimated_value = models.PositiveIntegerField(default=0)

    ltv = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    term_years = models.PositiveIntegerField(default=0)
    term_months = models.PositiveIntegerField(default=0)
    outstanding_balance = models.DecimalField(
        max_digits=15, decimal_places=2, blank=True, null=True
    )
    current_monthly_payment = models.DecimalField(
        max_digits=15, decimal_places=2, blank=True, null=True
    )
    current_lender = models.CharField(
        max_length=50, choices=CurrentLenderChoices.choices, blank=True, null=True
    )

    interest_only_amount = models.DecimalField(
        max_digits=15, decimal_places=2, blank=True, null=True, default=0.00
    )
    original_purchase_price = models.DecimalField(
        max_digits=15, decimal_places=2, blank=True, null=True, default=0.00
    )
    date_of_purchase = models.DateField(null=True, blank=True)
    deposit_amount = models.PositiveIntegerField(default=0)
    deposit_source = models.CharField(max_length=255, null=True, blank=True)
    advice_level = models.CharField(
        max_length=50, choices=AdviceLevelChoices.choices, blank=True, null=True
    )

    dip_accept_date = models.DateField(blank=True, null=True)
    dip_expiry_date = models.DateField(blank=True, null=True)
    expected_completion_date = models.DateField(blank=True, null=True)
    product_expiry_date = models.DateField(blank=True, null=True)

    introduction_type = models.CharField(
        max_length=50, choices=IntroductionTypeChoices.choices, blank=True, null=True
    )
    introducer_payment_terms = models.CharField(
        max_length=50,
        choices=IntroducerPaymentTermsChoices.choices,
        blank=True,
        null=True,
    )
    introducer_fee = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    lead_source = models.CharField(
        max_length=50, choices=LeadSourceChoices.choices, blank=True, null=True
    )
    sale_type = models.CharField(
        max_length=50, choices=SaleTypeChoices.choices, blank=True, null=True
    )
    reasons_for_capital_raising = models.TextField(blank=True, null=True)
    case_summary = models.TextField(blank=True, null=True)
    accepted_or_declined_by_lender = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_at", "-updated_at"]
        verbose_name = "Loan Detail"
        verbose_name_plural = "Loan Details"

    def __str__(self):
        return f"{self.application_type} - {self.mortgage_type if self.mortgage_type else 'No Mortgage Type'}"


class ApplicantDetails(CreatedAtUpdatedAtBaseModel):
    case = models.ForeignKey(
        Case,
        on_delete=models.CASCADE,
        related_name="applicant_details",
    )
    is_company_application = models.BooleanField(default=False)

    applicant = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="applicant",
    )
    title = models.CharField(
        max_length=10, choices=TitleChoices.choices, default=TitleChoices.MR
    )

    maiden_name = models.CharField(max_length=100, blank=True, null=True)
    date_of_birth = models.DateField(null=True, blank=True)
    anticipated_retirement_age = models.PositiveIntegerField(default=0)
    state_retirement_age = models.PositiveIntegerField(default=0)
    is_smoker = models.BooleanField(default=False)
    gender = models.CharField(
        max_length=6, choices=GenderChoices.choices, default=GenderChoices.MALE
    )
    nationality = CountryField(blank_label="Select Country", blank=True, null=True)
    is_dual_nationality = models.BooleanField(default=False)
    dual_nationality = CountryField(blank_label="Select Country", blank=True, null=True)
    marital_status = models.CharField(
        max_length=30,
        choices=MaritalStatusChoices.choices,
        default=MaritalStatusChoices.SINGLE,
    )
    dual_nationality_country = CountryField(
        blank_label="Select Country", blank=True, null=True
    )
    ni_number = models.CharField(max_length=20, blank=True, null=True)
    country_of_birth = models.CharField(max_length=100, blank=True, null=True)
    bank_name = models.CharField(max_length=100, blank=True, null=True)
    home_phone = models.CharField(max_length=20, blank=True, null=True)
    mobile_phone = models.CharField(max_length=20, blank=True, null=True)
    work_phone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

    marketing_preferences = MultiSelectField(
        choices=MarketingPreferencesChoices.choices, max_length=100, blank=True
    )
    has_dependants = models.BooleanField(default=False)
    number_of_dependants = models.PositiveIntegerField(default=0)
    date_of_arrival_uk = models.DateField(blank=True, null=True)
    indefinite_right_to_reside = models.BooleanField(default=False)
    visa_details = models.CharField(max_length=255, blank=True, null=True)
    visa_expiry_date = models.DateField(blank=True, null=True)
    postcode = models.CharField(max_length=10, null=True, blank=True)
    house_number_or_name = models.CharField(max_length=255, blank=True, null=True)
    address_line1 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    county = models.CharField(max_length=100, blank=True, null=True)
    county = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    effective_from = models.DateField(blank=True, null=True)
    time_at_address_years = models.PositiveIntegerField(default=0)
    time_at_address_months = models.PositiveIntegerField(default=0)
    residential_status = models.CharField(
        max_length=50,
        choices=ResidentialStatus.choices,
        default=ResidentialStatus.OWNER,
    )
    current_mortgage_balance = models.DecimalField(
        max_digits=12, decimal_places=2, default=0.00
    )
    property_value = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    owner_monthly_payment = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00
    )
    lender = models.CharField(max_length=100, blank=True, null=True)
    mortgage_start_date = models.DateField(blank=True, null=True)
    mortgage_type = models.CharField(
        max_length=100, choices=MortgageType.choices, default=MortgageType.SECURED_LOAN
    )
    current_interest_rate = models.DecimalField(
        max_digits=5, decimal_places=2, default=0.00
    )
    remaining_term = models.PositiveIntegerField(default=0)
    repayment_type = models.CharField(
        max_length=50,
        choices=RepaymentType.choices,
        default=RepaymentType.CAPITAL_INTEREST,
    )
    current_interest_type = models.CharField(
        max_length=50, choices=InterestType.choices, default=InterestType.FIXED
    )
    early_repayment_charge_applies = models.BooleanField(default=False)
    erc_expiry_date = models.DateField(null=True, blank=True)
    erc_amount = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    erc_being_paid = models.BooleanField(default=False)
    mortgage_account_number = models.CharField(max_length=50, blank=True, null=True)
    being_redeemed = models.BooleanField(default=False)
    is_mortgage_portable = models.BooleanField(default=False)
    is_mortgage_being_ported = models.BooleanField(default=False)
    mortgage_not_to_complete_until_erc_ended = models.CharField(
        max_length=10, choices=ERCCompletionStatus.choices, null=True, blank=True
    )
    mortgage_charter_scheme = models.BooleanField(default=False)
    property_type = models.CharField(
        max_length=50, choices=PropertyType.choices, default=PropertyType.HOUSE
    )
    bedrooms = models.PositiveIntegerField(default=0)
    tenure = models.CharField(
        max_length=50, choices=TenureType.choices, default=TenureType.FREEHOLD
    )
    year_built = models.PositiveIntegerField(default=0)
    notes = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ["-created_at", "-updated_at"]
        verbose_name = "Applicant Detail"
        verbose_name_plural = "Applicant Details"

    def __str__(self):
        return f"{self.company} ({self.applicant})"


class CompanyInfo(models.Model):
    applicant_details = models.ForeignKey(
        ApplicantDetails, on_delete=models.CASCADE, related_name="company"
    )
    company_name = models.CharField(max_length=255)
    company_registration_number = models.CharField(max_length=50, unique=True)
    date_of_incorporation = models.DateField(blank=True, null=True)
    company_type = models.CharField(
        max_length=50,
        choices=CompanyType.choices,
        default=CompanyType.PRIVATE_LIMITED,
    )
    trade_business_type = models.CharField(max_length=255, blank=True, null=True)
    sic_code = models.CharField(max_length=255, blank=True, null=True)
    is_spv = models.BooleanField(default=False)

    # Address fields
    postcode = models.CharField(max_length=20, blank=True, null=True)
    house_number_or_name = models.CharField(max_length=255, blank=True, null=True)
    address_line1 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    county = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.company_name} ({self.company_registration_number})"


class Dependant(models.Model):
    applicant_details = models.ForeignKey(
        ApplicantDetails, on_delete=models.CASCADE, related_name="dependants"
    )
    name = models.CharField(max_length=255)
    date_of_birth = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.date_of_birth})"


class DirectorShareholder(models.Model):
    company = models.ForeignKey(
        CompanyInfo, on_delete=models.CASCADE, related_name="directors_shareholders"
    )
    full_name = models.CharField(max_length=255, blank=True, null=True)
    percentage_share = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    role = models.CharField(
        max_length=50, choices=RoleType.choices, default=RoleType.DIRECTOR
    )

    def __str__(self):
        return f"{self.full_name} - {self.role} ({self.percentage_share}%)"


class EmploymentDetails(CreatedAtUpdatedAtBaseModel):
    case = models.ForeignKey(
        Case,
        on_delete=models.CASCADE,
        related_name="employment_details",
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="employment_details",
    )
    employment_status = models.CharField(
        max_length=50,
        choices=EmploymentStatus.choices,
        default=EmploymentStatus.EMPLOYED,
    )

    # For 'Employed' only:
    employment_type = models.CharField(
        max_length=50, choices=EmploymentType.choices, blank=True, null=True
    )
    occupation = models.CharField(max_length=255, blank=True, null=True)
    industry = models.CharField(max_length=255, blank=True, null=True)
    employer_name = models.CharField(max_length=255, blank=True, null=True)
    employer_telephone = models.CharField(max_length=255, blank=True, null=True)
    employer_email_for_reference = models.EmailField(blank=True, null=True)
    employer_postcode = models.CharField(max_length=20, blank=True, null=True)
    employer_house_name_or_number = models.CharField(
        max_length=255, blank=True, null=True
    )
    employer_address_line_1 = models.CharField(max_length=255, blank=True, null=True)
    employer_address_line_2 = models.CharField(max_length=255, blank=True, null=True)
    employer_city = models.CharField(max_length=255, blank=True, null=True)
    employer_county = models.CharField(max_length=255, blank=True, null=True)
    employer_country = models.CharField(max_length=255, blank=True, null=True)
    employment_commenced = models.DateField(blank=True, null=True)
    employment_ended = models.DateField(blank=True, null=True)

    gross_annual_income = models.DecimalField(
        max_digits=12, decimal_places=2, blank=True, null=True
    )
    net_annual_income = models.DecimalField(
        max_digits=12, decimal_places=2, blank=True, null=True
    )

    is_probationary_period = models.BooleanField(default=False)
    is_income_in_foreign_currency = models.BooleanField(default=False)

    bonus = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    is_bonus_guaranteed = models.BooleanField(default=False)
    bonus_frequency = models.CharField(
        max_length=50, choices=FrequencyChoice.choices, blank=True, null=True
    )

    overtime = models.DecimalField(
        max_digits=12, decimal_places=2, blank=True, null=True
    )
    is_overtime_guaranteed = models.BooleanField(default=False)
    overtime_frequency = models.CharField(
        max_length=50, choices=FrequencyChoice.choices, blank=True, null=True
    )

    allowance = models.DecimalField(
        max_digits=12, decimal_places=2, blank=True, null=True
    )
    is_allowance_guaranteed = models.BooleanField(default=False)
    allowance_frequency = models.CharField(
        max_length=50, choices=FrequencyChoice.choices, blank=True, null=True
    )

    # For 'Self-Employed' only:
    employment_time_year = models.PositiveIntegerField(blank=True, null=True, default=0)
    employment_time_month = models.PositiveIntegerField(
        blank=True, null=True, default=0
    )
    business_name = models.CharField(max_length=255, blank=True, null=True)
    business_telephone = models.CharField(max_length=255, blank=True, null=True)
    business_house_name_or_number = models.CharField(
        max_length=255, blank=True, null=True
    )
    business_postcode = models.CharField(max_length=20, blank=True, null=True)
    business_address_line_1 = models.CharField(max_length=255, blank=True, null=True)
    business_address_line_2 = models.CharField(max_length=255, blank=True, null=True)
    business_city = models.CharField(max_length=255, blank=True, null=True)
    business_county = models.CharField(max_length=255, blank=True, null=True)
    business_country = models.CharField(max_length=255, blank=True, null=True)
    job_title = models.CharField(max_length=255, blank=True, null=True)
    company_type = models.CharField(
        max_length=50, choices=CompanyType.choices, blank=True, null=True
    )
    percentage_of_business_owned = models.DecimalField(
        max_digits=5, decimal_places=2, blank=True, null=True
    )
    is_accounts_available = models.BooleanField(default=False)

    year1 = models.PositiveSmallIntegerField(
        blank=True, null=True, help_text="e.g. 2014"
    )
    year1_net_profit = models.PositiveIntegerField(
        default=0, help_text="Net profit for Year 1 (default is 0 if not provided)"
    )

    year2 = models.PositiveSmallIntegerField(
        blank=True, null=True, help_text="e.g. 2013"
    )
    year2_net_profit = models.PositiveIntegerField(
        default=0, help_text="Net profit for Year 2"
    )

    year3 = models.PositiveSmallIntegerField(
        blank=True, null=True, help_text="e.g. 2012"
    )
    year3_net_profit = models.PositiveIntegerField(
        default=0, help_text="Net profit for Year 3"
    )
    accountant_name = models.CharField(max_length=255, blank=True, null=True)
    accountant_qualifications = models.CharField(max_length=255, blank=True, null=True)
    salary = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    dividends = models.DecimalField(
        max_digits=12, decimal_places=2, blank=True, null=True
    )
    turnover = models.DecimalField(
        max_digits=12, decimal_places=2, blank=True, null=True
    )

    # For 'Retired':
    further_details = models.TextField(blank=True, null=True)
    income_source = models.CharField(max_length=255, blank=True, null=True)

    # For 'Other':
    other_income = models.DecimalField(
        max_digits=12, decimal_places=2, blank=True, null=True
    )
    other_income_source = models.CharField(max_length=255, blank=True, null=True)
    other_income_start_date = models.DateField(blank=True, null=True)

    # For 'Contractor':
    contractor_industry = models.CharField(max_length=255, blank=True, null=True)
    current_contract_start = models.DateField(blank=True, null=True)
    current_contract_end = models.DateField(blank=True, null=True)
    time_contracting = models.CharField(max_length=255, blank=True, null=True)
    day_rate = models.DecimalField(
        max_digits=12, decimal_places=2, blank=True, null=True
    )
    hourly_rate = models.DecimalField(
        max_digits=12, decimal_places=2, blank=True, null=True
    )

    def __str__(self):
        return f"{self.employment_status}"


class Adverse(CreatedAtUpdatedAtBaseModel):
    case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name="adverse")
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="adverse_user"
    )
    has_any_defaults_registered_in_the_last_six_years = models.BooleanField(
        default=False
    )

    has_any_ccj_registered_in_the_last_six_years = models.BooleanField(default=False)

    missed_any_payments_on_commitments_in_the_last_five_years = models.BooleanField(
        default=False
    )

    is_a_property_repossessed = models.BooleanField(default=False)

    has_ever_been_made_bankrupt = models.BooleanField(default=False)
    have_you_ever_entered_into_an_individual_voluntary_arrangement = (
        models.BooleanField(default=False)
    )
    is_ever_enter_into_a_debt_management_plan_or_debt_relief_order = (
        models.BooleanField(default=False)
    )

    is_ever_taken_out_a_pay_day_loan = models.BooleanField(default=False)

    is_exceeded_your_overdraft_in_the_last_three_months = models.BooleanField(
        default=False
    )
    is_direct_debit_returned_in_the_last_three_months = models.BooleanField(
        default=False
    )
    why_did_the_adverse_occur = models.CharField(max_length=500, blank=True, null=True)


class Property(CreatedAtUpdatedAtBaseModel):
    case = models.ForeignKey(
        Case,
        on_delete=models.CASCADE,
        related_name="property",
    )

    applicant = models.ManyToManyField(
        User,
        related_name="applicant_property",
    )
    is_property_owner = models.BooleanField(default=False)
    postcode = models.CharField(max_length=255)
    house_name_or_number = models.CharField(max_length=255)
    address_1 = models.CharField(max_length=255)
    address_2 = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=255)
    county = models.CharField(max_length=255, null=True, blank=True)
    country = models.CharField(max_length=255)

    property_value = models.DecimalField(max_digits=12, decimal_places=2)
    current_mortgage_balance = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True
    )
    monthly_rental_income = models.DecimalField(max_digits=12, decimal_places=2)
    monthly_mortgage_payment = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True
    )
    value_at_purchase = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True
    )
    date_purchased = models.DateField(null=True, blank=True)
    is_hmo = models.BooleanField(default=False)
    is_mufb = models.BooleanField(default=False)

    mortgage_lender = models.CharField(max_length=255, null=True, blank=True)
    repayment_type = models.CharField(max_length=255, null=True, blank=True)
    to_be_repaid = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True
    )

    current_rate = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True
    )
    rate_type = models.CharField(
        max_length=255, choices=RateTypeChoices.choices, null=True, blank=True
    )
    current_rate_end_date = models.DateField(null=True, blank=True)
    erc_end_date = models.DateField(null=True, blank=True)

    account_number = models.CharField(max_length=255, null=True, blank=True)
    property_type = models.CharField(max_length=255)
    ownership = models.CharField(max_length=255)
    leasehold = models.IntegerField(null=True, blank=True)  # Years
    year_built = models.IntegerField(null=True, blank=True)
    number_of_bedrooms = models.IntegerField()
    remaining_mortgage_term = models.IntegerField(null=True, blank=True)  # Years
    is_limited_company = models.BooleanField(default=False)
    epc_rating = models.CharField(
        max_length=255, choices=EPCRatingChoices.choices, null=True, blank=True
    )

    class Meta:
        ordering = ("-created_at", "-updated_at")

    def __str__(self):
        return f"Property {self.alias} - {self.property_value} ({self.city}, {self.country})"



class SolicitorAccountant(CreatedAtUpdatedAtBaseModel):
    case = models.ForeignKey(
        Case,
        on_delete=models.CASCADE,
        related_name="solicitor_accountant",
    )
    name = models.CharField(max_length=255)
    user_type = models.CharField(choices=UserTypeChoices.choices, max_length=255, default=UserTypeChoices.Accountant)
    sra_number = models.CharField(max_length=255, null=True, blank=True)
    postcode = models.CharField(max_length=255)
    building_name_or_number = models.CharField(max_length=255, null=True, blank=True)
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    county = models.CharField(max_length=255, null=True, blank=True)
    country = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=255, null=True, blank=True)
    fax_number = models.CharField(max_length=255)
    dx_number = models.CharField(max_length=255)
    contact_name = models.CharField(max_length=255)
    email_address = models.CharField(max_length=255, null=True, blank=True)
    number_of_partners_in_firm = models.IntegerField(null=True, blank=True)
    qualifications = models.CharField(max_length=255)

    class Meta:
        ordering = ("-created_at", "-updated_at")

    def __str__(self):
        return f"SolicitorAccountant {self.alias} - {self.user_type} - {self.sra_number} ({self.city}, {self.country})"

#existing-protection
class ExistingProtection(CreatedAtUpdatedAtBaseModel):
    have_any_existing_Protection_policies_in_place = models.BooleanField(default=False)
    policy_type = models.CharField(max_length=255, choices=ProductCategoryChoices.choices, null=True, blank=True)
    policy_provider = models.CharField(max_length=255, null=True, blank=True)
    insurers_reference = models.CharField(max_length=255, null=True, blank=True)
    sum_assured = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    premium = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    premium_payment_type = models.CharField(max_length=255, choices=PremiumPaymentChoices.choices, null=True, blank=True)
    person_assured = models.CharField(max_length=255, null=True, blank=True)
    in_trust = models.CharField(max_length=255, choices=InTrustChoices.choices, null=True, blank=True)
    guaranteed_reviewable = models.CharField(max_length=255, choices=GuaranteedReviewableChoices.choices, null=True, blank=True)
    remaining_policy_term = models.CharField(max_length=255, null=True, blank=True)
    cancelled_lapsed_date = models.DateField(null=True, blank=True)
    renewal_date = models.DateField(null=True, blank=True)
    date_policy_started = models.DateField(null=True, blank=True)
    waiver_of_premium = models.BooleanField(default=False)
    indexation = models.BooleanField(default=False)
    death_in_service_provision = models.BooleanField(default=False)
    have_non_standard_terms_been_issued = models.BooleanField(default=False)
    copy_and_paste_non_standard_terms_from_lender = models.TextField(null=True, blank=True)
    will_this_policy_be_cancelled =models.BooleanField(default=False)
    reason_for_policy_cancellation = models.CharField(max_length=255,choices=PolicyCancellationChoices.choices, null=True, blank=True)
    policy_cancellation_notes = models.TextField(null=True, blank=True)
    why_did_you_take_out_this_policy =models.TextField(null=True, blank=True)

    class Meta:
        ordering = ("-created_at", "-updated_at")

    def __str__(self):
        return f"ExistingProtection {self.alias} - {self.policy_type} - {self.policy_provider}"

# Call all signals here.
post_save.connect(create_loan_details, sender=Case)
post_save.connect(create_applicant_details, sender=Case)
post_save.connect(create_applicant_details_for_joint_user, sender=JointUser)
post_save.connect(create_employment_details_for_lead, sender=Case)
post_save.connect(create_employment_details_for_joint_user, sender=JointUser)
post_save.connect(create_adverse_for_lead, sender=Case)
post_save.connect(create_adverse_for_joint_user, sender=JointUser)
