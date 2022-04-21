from django.test import TestCase
from references.models import Clinic, Department

from factories.references.clinics import ClinicFactory, DepartmentFactory
from factories.updates.updates import UpdateFactory
from factories.users import UserFactory


class BaseSoftDeletableManagerTest(TestCase):
    def setUp(self) -> None:
        self.clinic_1 = ClinicFactory()
        self.clinic_2 = ClinicFactory()
        self.clinic_3 = ClinicFactory()

    def test_delete_only_soft_deletes_clinics(self):
        """
        Test that model isn't actually deleted, but only soft-deleted.

        """
        self.clinic_1.delete()
        self.assertTrue(Clinic.all_objects.filter(id=self.clinic_1.id).exists())
        self.assertTrue(Clinic.all_objects.filter(id=self.clinic_2.id).exists())
        self.clinic_1.refresh_from_db()
        self.assertTrue(self.clinic_1.is_deleted)

    def test_that_default_queryset_exclude_soft_deleted_objects(self):
        """
        Test that default queryset `objects` doesn't include deleted
        objects. And that `all_objects` does.
        """
        self.clinic_1.delete()
        self.assertQuerysetEqual(
            Clinic.objects.all(),
            [self.clinic_2.id, self.clinic_3.id],
            transform=lambda x: x.id,
            ordered=False,
        )
        self.assertQuerysetEqual(
            Clinic.all_objects.all(),
            [self.clinic_1.id, self.clinic_2.id, self.clinic_3.id],
            transform=lambda x: x.id,
            ordered=False,
        )


class BestUpdatableManagerTest(TestCase):
    def test_update_or_create_from_dict__new(self):
        """Test that new instance is created"""
        ClinicFactory(external_id=42)
        identifiers = ["external_id"]
        data = {
            "external_id": 43,
            "abbreviation": "AMB",
            "description": "Ambulance",
            "is_hospital": True,
            "is_ambulance": True,
        }

        clinic, operation = Clinic.objects.update_or_create_from_dict(
            identifiers=identifiers,
            data=data,
        )

        self.assertEqual(Clinic.objects.count(), 2)

        expected = Clinic.objects.get(external_id=43)
        self.assertEqual(clinic, expected)
        self.assertEqual(operation, Clinic.objects.CREATED)
        self.assertEqual(expected.abbreviation, "AMB")
        self.assertEqual(expected.description, "Ambulance")

    def test_update_or_create_from_dict__existing(self):
        """Test that existing instance that have differences is updated"""
        ClinicFactory(
            external_id=42,
            abbreviation="CL",
            description="Clinic",
        )
        identifiers = ["external_id"]
        data = {
            "external_id": 42,
            "abbreviation": "CLN",
            "description": "Clinic new",
        }

        clinic, operation = Clinic.objects.update_or_create_from_dict(identifiers, data)

        self.assertEqual(Clinic.objects.count(), 1)

        expected = Clinic.objects.get(external_id=42)
        self.assertEqual(clinic, expected)
        self.assertEqual(operation, Clinic.objects.UPDATED)
        self.assertEqual(expected.abbreviation, "CLN")
        self.assertEqual(expected.description, "Clinic new")

    def test_update_or_create_from_dict__existing_without_difference(self):
        """Test that existing instance that have differences is updated"""
        ClinicFactory(
            external_id=42,
            abbreviation="CL",
            description="Clinic",
        )
        identifiers = ["external_id"]
        data = {
            "external_id": 42,
            "abbreviation": "CL",
            "description": "Clinic",
        }

        clinic, operation = Clinic.objects.update_or_create_from_dict(identifiers, data)

        self.assertEqual(Clinic.objects.count(), 1)

        expected = Clinic.objects.get(external_id=42)
        self.assertEqual(clinic, expected)
        self.assertEqual(operation, Clinic.objects.NOT_CHANGED)
        self.assertEqual(expected.abbreviation, "CL")
        self.assertEqual(expected.description, "Clinic")

    def test_update_or_create_from_dict__set_history_user(self):
        """Test that method (optionally) set history user"""
        user = UserFactory(username="updater")
        identifiers = ["external_id"]
        data = {
            "external_id": 43,
            "abbreviation": "CLN",
            "description": "Clinic new",
        }

        clinic, _ = Clinic.objects.update_or_create_from_dict(
            identifiers, data, user=user
        )

        history = clinic.history.first()
        self.assertEqual(history.history_user, user)

    def test_update_or_create_from_dict__set_update_attribute(self):
        """Test that method (optionally) set update attribute"""
        user = UserFactory(username="updater")
        identifiers = ["external_id"]
        data = {
            "external_id": 43,
            "abbreviation": "CLN",
            "description": "Clinic new",
        }
        update = UpdateFactory()

        clinic, _ = Clinic.objects.update_or_create_from_dict(
            identifiers, data, user=user, update=update
        )

        history = clinic.history.first()
        self.assertEqual(history.history_user, user)


class ClinicManagerTemporaryCreationTest(TestCase):
    # Test BaseTemporaryCreatableManager methods
    def test_get_or_create_tmp__existing(self):
        """Test that get_or_create_tmp return existing object"""

        initial_clinic = ClinicFactory()

        clinic, created = Clinic.objects.get_or_create_temporary(
            external_id=initial_clinic.external_id
        )

        self.assertEqual(created, False)
        self.assertEqual(
            clinic,
            initial_clinic,
        )

    def test_get_or_create_tmp__new(self):
        """Test that get_or_create_tmp create new temporary object"""

        clinic, created = Clinic.objects.get_or_create_temporary(external_id=42)

        self.assertEqual(created, True)
        self.assertEqual(clinic.external_id, 42)
        self.assertEqual(clinic.description, "TMP")
        self.assertEqual(clinic.abbreviation, "TMP")


class BestUpdatableManagerTest(TestCase):
    """Test update_or_create_from_dict"""

    def test_update_or_create_from_dict__new_related_instance(self):
        """Test that new instance is created"""
        identifiers = ["external_id"]
        relations = {
            "clinic_external_id": {
                "field": "clinic",
                "key": "external_id",
                "delete_source_field": True,
            }
        }
        data = {
            "id": 172,
            "clinic_external_id": 42,
            "external_id": 78,
            "abbreviation": "DPT",
            "description": "Departament",
        }
        department, operation = Department.objects.update_or_create_from_dict(
            identifiers=identifiers,
            data=data,
            relations=relations,
        )

        self.assertEqual(Department.objects.count(), 1)

        expected = Department.objects.get(external_id=78)
        self.assertEqual(department, expected)
        self.assertEqual(operation, Department.objects.CREATED)

        self.assertEqual(Clinic.objects.count(), 1)
        self.assertEqual(department.clinic.external_id, 42)
        self.assertEqual(department.clinic.description, "TMP")
