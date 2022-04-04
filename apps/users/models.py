from common.models import BaseHistoricalModel
from django.contrib.auth.models import AbstractUser
from django.db import models
from users.managers import UserManager


class User(AbstractUser, BaseHistoricalModel):
    is_system = models.BooleanField(default=False)

    objects = UserManager()
