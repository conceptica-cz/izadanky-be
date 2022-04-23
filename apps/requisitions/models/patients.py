import logging

from django.db import models
from updates.managers import BaseUpdatableManager
from updates.models import BaseUpdatableModel

logger = logging.getLogger(__name__)


class Patient(BaseUpdatableModel):
    birth_number = models.CharField(unique=True, max_length=10, help_text="Rodné číslo")
    external_id = models.CharField(
        max_length=50, null=True, blank=True, unique=True, help_text="UNIS ID"
    )
    name = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)

    objects = BaseUpdatableManager()

    def __str__(self):
        return f"{self.name} ({self.pk})"
