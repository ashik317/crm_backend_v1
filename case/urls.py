from django.urls import path

from .common import RegisterLoan
from .models import LoanDetails
from .views import (
    CaseListCreateApiView,
    CaseRetrieveUpdateDeleteApiView,
    FileListCreateApiView,
    FileRetrieveUpdateDeleteApiView,
    JointUserListCreateApiView,
    JointUserRetrieveUpdateDeleteApiView,
    CaseUserListApiView,
    LoanDetailsListCreateApiView,
    LoanDetailsRetrieveUpdateApiView,
    CaseUserListViewOnlyApiView,
    ApplicantDetailsListApiView,
    ApplicantDetailsRetrieveUpdateApiView,
    DependantListCreateApiView,
    CompanyInfoListCreateApiView,
    DirectorShareholderListCreateApiView,
    EmploymentDetailsListApiView,
    EmploymentDetailsCreateApiView,
    EmploymentDetailsRetrieveUpdateApiView,
    AdverseListApiView,
    AdverseRetrieveUpdateApiView,
)

urlpatterns = [
    path("", CaseListCreateApiView.as_view(), name="case-list-create"),
    path(
        "<uuid:alias>/",
        CaseRetrieveUpdateDeleteApiView.as_view(),
        name="case-retrieve-update-delete",
    ),
    path(
        "<uuid:case_alias>/files/",
        FileListCreateApiView.as_view(),
        name="file-list-create",
    ),
    path(
        "<uuid:case_alias>/files/<uuid:alias>/",
        FileRetrieveUpdateDeleteApiView.as_view(),
        name="file-detail",
    ),
    path(
        "<uuid:case_alias>/joint/users/",
        JointUserListCreateApiView.as_view(),
        name="joint-user-list-create",
    ),
    path(
        "<uuid:case_alias>/joint/users/<uuid:alias>/",
        JointUserRetrieveUpdateDeleteApiView.as_view(),
        name="joint-user-detail",
    ),
    path(
        "<uuid:case_alias>/users/",
        CaseUserListApiView.as_view(),
        name="case-user-list",
    ),
    path(
        "<uuid:case_alias>/loan/details/",
        LoanDetailsListCreateApiView.as_view(),
        name="loan-details-list-create",
    ),
    path(
        "<uuid:case_alias>/loan/details/<uuid:alias>/",
        LoanDetailsRetrieveUpdateApiView.as_view(),
        name="loan-details-detail",
    ),
    path(
        "<uuid:case_alias>/user/list/",
        CaseUserListViewOnlyApiView.as_view(),
        name="case-users",
    ),
    path(
        "<uuid:case_alias>/applicant/details/",
        ApplicantDetailsListApiView.as_view(),
        name="applicant-details-list",
    ),
    path(
        "<uuid:case_alias>/applicant/details/<uuid:alias>/",
        ApplicantDetailsRetrieveUpdateApiView.as_view(),
        name="applicant-details-detail",
    ),
    path(
        "<uuid:case_alias>/applicant/details/<uuid:alias>/dependants/",
        DependantListCreateApiView.as_view(),
        name="dependant-list",
    ),
    path(
        "<uuid:case_alias>/applicant/details/<uuid:alias>/company/",
        CompanyInfoListCreateApiView.as_view(),
        name="companyinfo-list-create",
    ),
    path(
        "<uuid:case_alias>/applicant/details/<uuid:alias>/company/<str:company_name>/shareholders/",
        DirectorShareholderListCreateApiView.as_view(),
        name="director-shareholder-list-create",
    ),
    path(
        "<uuid:case_alias>/employment/details/",
        EmploymentDetailsListApiView.as_view(),
        name="employment-details-list",
    ),
    path(
        "<uuid:case_alias>/employment/details/<int:pk>",
        EmploymentDetailsCreateApiView.as_view(),
        name="employment-details-create",
    ),
    path(
        "<uuid:case_alias>/employment/details/<uuid:alias>/",
        EmploymentDetailsRetrieveUpdateApiView.as_view(),
        name="employment-details-detail",
    ),
    path(
        "<uuid:case_alias>/adverse/",
        AdverseListApiView.as_view(),
        name="adverse-list",
    ),
    path(
        "<uuid:case_alias>/adverse/<uuid:alias>/",
        AdverseRetrieveUpdateApiView.as_view(),
        name="adverse-detail",
    ),
    # path(
    #     "<uuid:case_alias>/adverse/<uuid:alias>/register/loans/",
    #     RegisterLoanListCreateApiView.as_view(),
    #     name="register-loan-list-create",
    # ),
    # path(
    #     "<uuid:case_alias>/adverse/<uuid:alias>/payment/commitments/",
    #     PaymentCommitmentListCreateApiView.as_view(),
    #     name="payment-commitment-list-create",
    # ),
    # path(
    #     "<uuid:case_alias>/adverse/<uuid:alias>/property/repossessed/",
    #     PropertyRepossessedListCreateApiView.as_view(),
    #     name="property-repossessed-list-create",
    # ),
    # path(
    #     "<uuid:case_alias>/adverse/<uuid:alias>/bankrupts/",
    #     BankruptListCreateApiView.as_view(),
    #     name="bankrupt-list-create",
    # ),
    # path(
    #     "<uuid:case_alias>/adverse/<uuid:alias>/individual/voluntary/",
    #     IndividualVoluntaryListCreateApiView.as_view(),
    #     name="individual-voluntary-list-create",
    # ),
    # path(
    #     "<uuid:case_alias>/adverse/<uuid:alias>/debt/management/",
    #     DebtManagementPlanListCreateApiView.as_view(),
    #     name="debt-management-list-create",
    # ),
    # path(
    #     "<uuid:case_alias>/adverse/<uuid:alias>/pay/day/loan/",
    #     PayDayLoanListCreateApiView.as_view(),
    #     name="pay-day-loan-list-create",
    # ),
]
