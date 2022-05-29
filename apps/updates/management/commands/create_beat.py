import json

from django.conf import settings
from django.core.management.base import BaseCommand
from django_celery_beat.models import IntervalSchedule, PeriodicTask

EXTERNAL_SOURCES = ["Patient"]


class Command(BaseCommand):
    help = "Create django celery beat periodic tasks"

    def add_arguments(self, parser):
        # Optional only external argument
        parser.add_argument(
            "--only-patient",
            action="store_true",
            help="Create only patient tasks",
        )

    def handle(self, *args, **options):
        print("Creating django celery beat periodic tasks...")
        for name in settings.UPDATE_SOURCES:
            self._create_reference_beat(name)
        self._create_delete_old_report_files_beat()
        self._create_delete_old_empty_updates_beat()
        print("Done.")

    @staticmethod
    def _create_reference_beat(name):
        interval_incremental = settings.UPDATE_SOURCES[name].get("interval_incremental")
        if interval_incremental:
            task_name = f"{name} incremental"
            if not PeriodicTask.objects.filter(name=task_name).exists():
                interval_schedule, _ = IntervalSchedule.objects.get_or_create(
                    every=interval_incremental,
                    period=IntervalSchedule.MINUTES,
                )
                PeriodicTask.objects.create(
                    name=task_name,
                    task="updates.tasks.update",
                    kwargs=json.dumps({"source_name": name}),
                    interval=interval_schedule,
                    enabled=False,
                )

        interval_full = settings.UPDATE_SOURCES[name].get("interval_full")
        if interval_full:
            task_name = f"{name} full"
            if not PeriodicTask.objects.filter(name=task_name).exists():
                interval_schedule, _ = IntervalSchedule.objects.get_or_create(
                    every=interval_full,
                    period=IntervalSchedule.MINUTES,
                )
                PeriodicTask.objects.create(
                    name=task_name,
                    task="updates.tasks.update",
                    kwargs=json.dumps({"source_name": name, "full_update": True}),
                    interval=interval_schedule,
                    enabled=False,
                )

    @staticmethod
    def _create_delete_old_report_files_beat():
        interval_schedule, _ = IntervalSchedule.objects.get_or_create(
            every=60,
            period=IntervalSchedule.MINUTES,
        )
        task_name = f"Delete old report files"
        PeriodicTask.objects.update_or_create(
            name=task_name,
            defaults={
                "task": "reports.tasks.delete_old_report_files",
                "interval": interval_schedule,
            },
        )

    @staticmethod
    def _create_delete_old_empty_updates_beat():
        interval_schedule, _ = IntervalSchedule.objects.get_or_create(
            every=1,
            period=IntervalSchedule.DAYS,
        )
        task_name = f"Delete old empty Updates and ModelUpdates"
        PeriodicTask.objects.update_or_create(
            name=task_name,
            defaults={
                "task": "updates.tasks.task_delete_old_emtpy_updates",
                "interval": interval_schedule,
            },
        )
