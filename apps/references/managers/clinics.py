from django.db.models import Count, Q
from updates.managers import BaseTemporaryCreatableManager


class ClinicManager(BaseTemporaryCreatableManager):
    TEMPORARY_DEFAULTS = {
        "description": "TMP",
        "abbreviation": "TMP",
    }

    def get_hospitals(self):
        """Return only hospital clinics"""
        return self.get_queryset().filter(is_hospital=True)

    def get_ambulances(self):
        """Return only ambulance clinics"""
        return self.get_queryset().filter(is_ambulance=True)
