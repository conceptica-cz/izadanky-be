from common.admin import BaseHistoryAdmin
from django.contrib import admin

from ..models.requisitions import Requisition


@admin.register(Requisition)
class RequisitionAdmin(BaseHistoryAdmin):
    list_display = [
        "id",
    ]
    search_fields = ["id"]
