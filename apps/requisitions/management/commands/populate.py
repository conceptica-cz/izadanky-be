from django.conf import settings
from django.core.management.base import BaseCommand

from factories.references import PersonFactory
from factories.users import UserFactory


class Command(BaseCommand):
    help = "Populate database with fake data"

    def handle(self, *args, **options):
        if settings.ENVIRONMENT not in ["test", "development", "local"]:
            self.stdout.write(
                self.style.ERROR(
                    "This command should only be used in test, local or development environments."
                )
            )
            return
        print("Populating database. Please wait...")
        users = []
        for i in range(1, 5):
            users.append(UserFactory(username=f"b{i}"))

        persons = []
        for i in range(20):
            persons.append(PersonFactory())

        print("Database was populated.")
