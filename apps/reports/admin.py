# Register your models here.
from common.admin import BaseHistoryAdmin
from django.contrib import admin
from reports import models


@admin.register(models.GenericReportType)
class GenericReportTypeAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "file_name", "frequency", "formats", "order")
    actions = ["generate"]

    @admin.action(description="Generate report")
    def generate(self, request, queryset):
        for report_type in queryset:
            report_type.generate_report()


@admin.register(models.GenericReportFile)
class GenericReportFileAdmin(admin.ModelAdmin):
    list_display = (
        "report_type",
        "report_format",
        "year",
        "month",
        "updated_at",
    )

    list_filter = ("report_type",)


@admin.register(models.ReportVariable)
class ReportVariableAdmin(BaseHistoryAdmin):
    list_display = (
        "report_type",
        "name",
        "description",
        "variable_type",
        "value",
        "order",
    )
    list_filter = ("report_type",)
