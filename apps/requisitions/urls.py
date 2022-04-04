from django.urls import path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from .views import clinics, reports, requisitions, tags, user

urlpatterns = [
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "schema/swagger-ui/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path("user/", user.UserView.as_view(), name="user"),
    path("clinics/", clinics.ClinicListView.as_view(), name="clinic_list"),
    path("clinics/<int:pk>/", clinics.ClinicDetailView.as_view(), name="clinic_detail"),
    path("departments/", clinics.DepartmentListView.as_view(), name="department_list"),
    path(
        "departments/<int:pk>/",
        clinics.DepartmentDetailView.as_view(),
        name="department_detail",
    ),
    path(
        "requisitions/",
        requisitions.RequisitionListView.as_view(),
        name="requisition_list",
    ),
    path(
        "requisitions/<int:pk>/",
        requisitions.RequisitionDetailView.as_view(),
        name="requisition_detail",
    ),
    path(
        "requisitions/<int:pk>/history/",
        requisitions.RequisitionHistoryView.as_view(),
        name="requisition_history",
    ),
    path(
        "tags/",
        tags.TagListView.as_view(),
        name="tag_list",
    ),
    path(
        "tags/<int:pk>/",
        tags.TagDetailView.as_view(),
        name="tag_detail",
    ),
    path(
        "reports/",
        reports.GenericReportTypeListView.as_view(),
        name="report_list",
    ),
    path(
        "reports/<int:pk>/variables/",
        reports.ReportVariableListView.as_view(),
        name="report_variable_list",
    ),
    path(
        "reports/<int:pk>/generate/",
        reports.ReportGenerateView.as_view(),
        name="report_generate",
    ),
    path(
        "report-variables/<int:pk>/",
        reports.ReportVariableDetailView.as_view(),
        name="report_variable_detail",
    ),
]
