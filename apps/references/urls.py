from django.urls import path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from .views import clinics, persons

app_name = "references"

urlpatterns = [
    path("clinics/", clinics.ClinicListView.as_view(), name="clinic_list"),
    path("clinics/<int:pk>/", clinics.ClinicDetailView.as_view(), name="clinic_detail"),
    path("departments/", clinics.DepartmentListView.as_view(), name="department_list"),
    path(
        "departments/<int:pk>/",
        clinics.DepartmentDetailView.as_view(),
        name="department_detail",
    ),
    path("persons/", persons.PersonListView.as_view(), name="person_list"),
    path("persons/<int:pk>/", persons.PersonDetailView.as_view(), name="person_detail"),
]
