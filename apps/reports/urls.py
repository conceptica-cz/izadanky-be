from django.urls import path

from . import views

app_name = "reports"

urlpatterns = [
    path(
        "reports/",
        views.GenericReportTypeListView.as_view(),
        name="report_list",
    ),
    path(
        "reports/<int:pk>/variables/",
        views.ReportVariableListView.as_view(),
        name="report_variable_list",
    ),
    path(
        "reports/<int:pk>/generate/",
        views.ReportGenerateView.as_view(),
        name="report_generate",
    ),
    path(
        "report-variables/<int:pk>/",
        views.ReportVariableDetailView.as_view(),
        name="report_variable_detail",
    ),
]
