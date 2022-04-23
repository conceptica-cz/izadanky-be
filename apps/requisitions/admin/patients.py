from common.admin import BaseHistoryAdmin
from django.contrib import admin

from ..models.patients import Patient


@admin.register(Patient)
class PatientAdmin(BaseHistoryAdmin):
    list_display = [
        "id",
        "birth_number",
        "external_id",
        "name",
    ]
    search_fields = ["id"]
