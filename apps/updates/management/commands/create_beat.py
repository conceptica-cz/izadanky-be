import json

from django.conf import settings
from django.core.management.base import BaseCommand
from django_celery_beat.models import CrontabSchedule, IntervalSchedule, PeriodicTask
from references.models import Clinic

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
        print("Done.")

    @staticmethod
    def _create_reference_beat(name):
        interval_schedule, _ = IntervalSchedule.objects.get_or_create(
            every=settings.UPDATE_SOURCES[name].get(
                "interval", settings.DEFAULT_INCREMENTAL_UPDATE_INTERVAL
            ),
            period=IntervalSchedule.MINUTES,
        )
        task_name = f"{name} incremental"
        PeriodicTask.objects.update_or_create(
            name=task_name,
            defaults={
                "task": "updates.tasks.update",
                "interval": interval_schedule,
                "kwargs": json.dumps({"source_name": name}),
            },
        )
        task_name = f"{name} full"
        full_schedule, _ = IntervalSchedule.objects.get_or_create(
            every=settings.UPDATE_SOURCES[name].get(
                "interval", settings.DEFAULT_FULL_UPDATE_INTERVAL
            ),
            period=IntervalSchedule.MINUTES,
        )
        PeriodicTask.objects.update_or_create(
            name=task_name,
            defaults={
                "task": "updates.tasks.update",
                "interval": full_schedule,
                "kwargs": json.dumps({"source_name": name, "full_update": True}),
            },
        )
