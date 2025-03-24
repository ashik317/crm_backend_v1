from django.db.models.signals import post_save
from django.dispatch import receiver
from django.apps import apps


@receiver(post_save, sender="case.Case")  # Change sender to string
def create_loan_details(sender, instance, created, **kwargs):
    if created:
        LoanDetails = apps.get_model("case", "LoanDetails")  # Move this inside function
        LoanDetails.objects.create(case=instance)


@receiver(
    post_save, sender="case.Case"
)  # Using string reference for dynamic model loading
def create_applicant_details(sender, instance, created, **kwargs):
    if created:
        ApplicantDetails = apps.get_model(
            "case", "ApplicantDetails"
        )  # Dynamically get ApplicantDetails model

        # Ensure only one ApplicantDetails instance is created
        ApplicantDetails.objects.create(
            case=instance,
            applicant=instance.lead,  # Always assign the lead as the applicant
        )


@receiver(
    post_save, sender="case.JointUser"
)  # Using string reference for dynamic loading
def create_applicant_details_for_joint_user(sender, instance, created, **kwargs):
    if created:
        ApplicantDetails = apps.get_model(
            "case", "ApplicantDetails"
        )  # Get ApplicantDetails model dynamically

        # Create ApplicantDetails for the joint user
        ApplicantDetails.objects.create(
            case=instance.case,
            applicant=instance.joint_user,  # Assigning the joint user as the applicant
        )


@receiver(post_save, sender="case.Case")
def create_employment_details_for_lead(sender, instance, created, **kwargs):
    """
    When a new Case is created, automatically create an EmploymentDetails record
    for the 'lead' user.
    """
    if created:
        EmploymentDetails = apps.get_model("case", "EmploymentDetails")
        EmploymentDetails.objects.create(
            case=instance,
            user=instance.lead,
            # Optionally set default values for some fields here
        )


@receiver(post_save, sender="case.JointUser")
def create_employment_details_for_joint_user(sender, instance, created, **kwargs):
    """
    When a new JointUser is created for a case, automatically create an EmploymentDetails
    record for that joint user.
    """
    if created:
        EmploymentDetails = apps.get_model("case", "EmploymentDetails")
        EmploymentDetails.objects.create(
            case=instance.case,
            user=instance.joint_user,
            # Optionally set default values for some fields here
        )


@receiver(post_save, sender="case.Case")
def create_adverse_for_lead(sender, instance, created, **kwargs):
    """
    When a new Case is created, automatically create an EmploymentDetails record
    for the 'lead' user.
    """
    if created:
        Adverse = apps.get_model("case", "Adverse")
        Adverse.objects.create(
            case=instance,
            user=instance.lead,
            # Optionally set default values for some fields here
        )


@receiver(post_save, sender="case.JointUser")
def create_adverse_for_joint_user(sender, instance, created, **kwargs):
    """
    When a new JointUser is created for a case, automatically create an EmploymentDetails
    record for that joint user.
    """
    if created:
        Adverse = apps.get_model("case", "Adverse")
        Adverse.objects.create(
            case=instance.case,
            user=instance.joint_user,
            # Optionally set default values for some fields here
        )


@receiver(post_save, sender="case.Case")
def create_existing_protection_for_lead(sender, instance, created, **kwargs):
    if created:
        ExistingProtection = apps.get_model("case", "ExistingProtection")
        ExistingProtection.objects.create(
            case=instance,
            user=instance.lead,
        )


@receiver(post_save, sender="case.JointUser")
def create_existing_protection_for_joint_user(sender, instance, created, **kwargs):
    if created:
        ExistingProtection = apps.get_model("case", "ExistingProtection")
        ExistingProtection.objects.create(
            case=instance.case,
            user=instance.joint_user,
        )


@receiver(post_save, sender="case.Case")
def create_property_details(sender, instance, created, **kwargs):

    if created:
        PropertyDetails = apps.get_model("case", "PropertyDetails")
        PropertyDetails.objects.create(case=instance)


@receiver(post_save, sender="case.Case")
def create_budget_planner(sender, instance, created, **kwargs):
    if created:
        BudgetPlanner = apps.get_model("case", "BudgetPlanner")
        BudgetPlanner.objects.create(case=instance)

# Mortgage Needs signal.
@receiver(post_save, sender="case.Case")
def create_mortgage_needs(sender, instance, created, **kwargs):
    if created:
        MortgageNeeds = apps.get_model("case", "MortgageNeeds")
        MortgageNeeds.objects.create(case=instance)

# MortgageFeatures signal.
@receiver(post_save, sender="case.Case")
def create_mortgage_features_for_lead(sender, instance, created, **kwargs):
    if created:
        MortgageFeatures = apps.get_model("case", "MortgageFeatures")
        MortgageFeatures.objects.create(
            case=instance,
            applicant=instance.lead,
        )

# @receiver(post_save, sender="case.JointUser")
# def create_mortgage_features_for_joint_user(sender, instance, created, **kwargs):
#     if created:
#         MortgageFeatures = apps.get_model("case", "MortgageFeatures")
#         MortgageFeatures.objects.create(
#             case=instance.case,
#             applicant=instance.joint_user,
#         )
