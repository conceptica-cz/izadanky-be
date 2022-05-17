import re
from typing import Optional

from common.models import BaseHistoricalModel
from django.contrib.auth.models import AbstractUser
from django.db import models
from users.managers import UserManager


class User(AbstractUser, BaseHistoricalModel):
    is_system = models.BooleanField(default=False)
    is_app = models.BooleanField(default=False)

    objects = UserManager()

    def get_person(self) -> Optional["Person"]:
        pattern = re.compile("^(b|ba)(\d+)")
        if not (match := pattern.match(self.username)):
            return None
        person_number = match.group(2)
        from references.models import Person

        person = Person.objects.filter(person_number=person_number).first()
        return person
