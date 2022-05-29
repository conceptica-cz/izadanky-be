from unittest.mock import Mock, patch

from django.test import TestCase
from django.utils import timezone
from updates.serializers import ModelChangeSerializer

from factories.references import ClinicFactory
from factories.users import UserFactory


class ModelChangeSerializerTest(TestCase):
    @patch("simple_history.models.timezone.now")
    def test_get_changes(self, mocked_now: Mock):
        initial_time = timezone.datetime(2020, 1, 1, 0, tzinfo=timezone.utc)
        mocked_now.return_value = initial_time
        clinic = ClinicFactory(abbreviation="a", description="d")
        user_1 = UserFactory()
        user_2 = UserFactory()

        change_time = timezone.datetime(2020, 1, 1, 2, tzinfo=timezone.utc)
        mocked_now.return_value = change_time

        clinic.abbreviation = "a2"
        clinic.description = "d2"
        clinic.save()
        history_record = clinic.history.first()
        history_record.history_user = user_2
        history_record.save()

        change = list(clinic.get_changes())[0]

        serializer = ModelChangeSerializer(change)

        self.assertEqual(
            serializer.data,
            {
                "entity_id": clinic.id,
                "entity_name": "Clinic",
                "date": "2020-01-01T03:00:00+01:00",
                "user": {
                    "id": user_2.id,
                    "username": user_2.username,
                    "first_name": user_2.first_name,
                    "last_name": user_2.last_name,
                    "email": user_2.email,
                },
                "field_changes": [
                    {
                        "field": "abbreviation",
                        "old_value": "a",
                        "new_value": "a2",
                    },
                    {
                        "field": "description",
                        "old_value": "d",
                        "new_value": "d2",
                    },
                ],
            },
        )
