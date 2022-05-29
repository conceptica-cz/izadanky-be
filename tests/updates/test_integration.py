from unittest.mock import Mock, patch

from django.test import TestCase, override_settings
from references.models import Clinic, Department
from updates.tasks import update

from factories.references import ClinicFactory, DepartmentFactory


@patch("updates.common.loaders.requests.get")
@override_settings(CELERY_TASK_ALWAYS_EAGER=True)
class TestClinicUpdate(TestCase):
    def test_clinic(self, mocked_get):
        ClinicFactory(reference_id=20, external_id=10)
        ClinicFactory(reference_id=21, external_id=11)
        response_data = {
            "results": [
                {
                    "id": 21,
                    "external_id": 41,
                    "abbreviation": "C1",
                    "description": "Clinic 1",
                    "is_hospital": False,
                    "is_ambulance": True,
                },
                {
                    "id": 22,
                    "external_id": 42,
                    "abbreviation": "C2",
                    "description": "Clinic 2",
                    "is_hospital": True,
                    "is_ambulance": False,
                },
            ],
        }
        mocked_get.return_value = Mock(
            status_code=200, json=Mock(return_value=response_data)
        )
        update("Clinic")

        self.assertEqual(Clinic.objects.count(), 3)

        clinic_1 = Clinic.objects.get(reference_id=21)
        self.assertEqual(clinic_1.external_id, 41)
        self.assertEqual(clinic_1.abbreviation, "C1")
        self.assertEqual(clinic_1.description, "Clinic 1")
        self.assertEqual(clinic_1.is_hospital, False)
        self.assertEqual(clinic_1.is_ambulance, True)

        clinic_2 = Clinic.objects.get(reference_id=22)
        self.assertEqual(clinic_2.external_id, 42)
        self.assertEqual(clinic_2.abbreviation, "C2")
        self.assertEqual(clinic_2.description, "Clinic 2")
        self.assertEqual(clinic_2.is_hospital, True)
        self.assertEqual(clinic_2.is_ambulance, False)


@patch("updates.common.loaders.requests.get")
@override_settings(CELERY_TASK_ALWAYS_EAGER=True)
class TestDepartmentUpdate(TestCase):
    def test_department(self, mocked_get):
        clinic = ClinicFactory(reference_id=41, external_id=51)
        DepartmentFactory(external_id=20, clinic=clinic)
        DepartmentFactory(external_id=21, clinic=clinic)
        clinic = ClinicFactory(reference_id=42, external_id=52)
        DepartmentFactory(external_id=22, clinic=clinic)
        response_data = {
            "results": [
                {
                    "id": 1,
                    "clinic": 41,
                    "external_id": 21,
                    "abbreviation": "D1",
                    "description": "Department 1",
                    "specialization_code": "111",
                    "icp": "111111",
                },
                {
                    "id": 2,
                    "clinic": 43,
                    "external_id": 22,
                    "abbreviation": "D2",
                    "description": "Department 2",
                    "specialization_code": "222",
                    "icp": "222222",
                },
                {
                    "id": 3,
                    "clinic": 43,
                    "external_id": 23,
                    "abbreviation": "D3",
                    "description": "Department 3",
                    "specialization_code": "333",
                    "icp": "333333",
                },
            ],
        }
        mocked_get.return_value = Mock(
            status_code=200, json=Mock(return_value=response_data)
        )
        update("Department")

        self.assertEqual(Department.objects.count(), 4)
        self.assertEqual(Clinic.objects.count(), 3)

        clinic_1 = Clinic.objects.get(reference_id=41)
        clinic_2 = Clinic.objects.get(reference_id=42)
        clinic_3 = Clinic.objects.get(reference_id=43)

        department_1 = Department.objects.get(external_id=21)
        self.assertEqual(department_1.external_id, 21)
        self.assertEqual(department_1.abbreviation, "D1")
        self.assertEqual(department_1.description, "Department 1")
        self.assertEqual(department_1.specialization_code, "111")
        self.assertEqual(department_1.icp, "111111")
        self.assertEqual(department_1.clinic, clinic_1)

        department_2 = Department.objects.get(external_id=22)
        self.assertEqual(department_2.external_id, 22)
        self.assertEqual(department_2.abbreviation, "D2")
        self.assertEqual(department_2.description, "Department 2")
        self.assertEqual(department_2.specialization_code, "222")
        self.assertEqual(department_2.icp, "222222")
        self.assertEqual(department_2.clinic, clinic_3)

        department_3 = Department.objects.get(external_id=23)
        self.assertEqual(department_3.external_id, 23)
        self.assertEqual(department_3.abbreviation, "D3")
        self.assertEqual(department_3.description, "Department 3")
        self.assertEqual(department_3.specialization_code, "333")
        self.assertEqual(department_3.icp, "333333")
        self.assertEqual(department_3.clinic, clinic_3)
