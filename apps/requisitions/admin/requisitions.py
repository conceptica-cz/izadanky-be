from common.admin import BaseHistoryAdmin
from django.contrib import admin

from ..models.requisitions import Requisition


@admin.register(Requisition)
class RequisitionAdmin(BaseHistoryAdmin):
    list_display = [
        "id",
        "state",
        "patient",
        "applicant",
        "created_by",
        "created_at",
        "updated_at",
    ]
    list_filter = ["state", "created_by"]
    search_fields = ["id"]
