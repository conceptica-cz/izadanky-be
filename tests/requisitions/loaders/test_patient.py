from django.test import TestCase, override_settings
from requisitions.loaders.patient import (
    APIError,
    APIisNotAvailable,
    Patient,
    PatientNotFound,
    load_patient,
)
from requisitions.models.patients import Patient as PatientModel
from requisitions.serializers.patients import PatientSerializer

from factories.requisitions import PatientFactory


def loader_returning_patient(birth_number, external_id):
    return Patient(
        birth_number="123456789",
        external_id="42",
        name="John Doe",
        first_name="John",
        last_name="Doe",
    )


def loader_raising_not_found(birth_number, external_id):
    raise PatientNotFound()


def loader_raising_api_error(birth_number, external_id):
    raise APIError()


def loader_raising_not_available(birth_number, external_id):
    raise APIisNotAvailable()


class LoadPatientTest(TestCase):
    @override_settings(
        PATIENT_LOADER="tests.requisitions.loaders.test_patient.loader_returning_patient"
    )
    def test_successful(self):

        result = load_patient(birth_number="123456789")

        added_patient = PatientModel.objects.first()
        self.assertEqual(added_patient.birth_number, "123456789")
        self.assertEqual(added_patient.external_id, "42")
        self.assertEqual(added_patient.name, "John Doe")
        self.assertEqual(added_patient.first_name, "John")
        self.assertEqual(added_patient.last_name, "Doe")

        self.assertEqual(result["data"], PatientSerializer(added_patient).data)
        self.assertEqual(result["success"], True)

    @override_settings(
        PATIENT_LOADER="tests.requisitions.loaders.test_patient.loader_returning_patient"
    )
    def test_successful_existing_patient(self):
        existing_patient = PatientFactory(
            birth_number="123456789",
            external_id="42",
            name="John Doe",
            first_name="John",
            last_name="Doe",
        )

        result = load_patient(birth_number="123456789")

        self.assertEqual(PatientModel.objects.count(), 1)
        added_patient = PatientModel.objects.first()

        self.assertEqual(result["data"], PatientSerializer(added_patient).data)
        self.assertEqual(result["success"], True)

    @override_settings(
        PATIENT_LOADER="tests.requisitions.loaders.test_patient.loader_raising_not_found"
    )
    def test_patient_not_found(self):

        result = load_patient(birth_number="123456789")

        self.assertEqual(PatientModel.objects.count(), 0)
        self.assertEqual(result["success"], False)
        self.assertEqual(result["error"], "PatientNotFound")

    @override_settings(
        PATIENT_LOADER="tests.requisitions.loaders.test_patient.loader_raising_api_error"
    )
    def test_api_error(self):

        result = load_patient(birth_number="123456789")

        self.assertEqual(PatientModel.objects.count(), 0)
        self.assertEqual(result["success"], False)
        self.assertEqual(result["error"], "APIError")

    @override_settings(
        PATIENT_LOADER="tests.requisitions.loaders.test_patient.loader_raising_not_available"
    )
    def test_api_not_available(self):

        result = load_patient(birth_number="123456789")

        self.assertEqual(PatientModel.objects.count(), 0)
        self.assertEqual(result["success"], False)
        self.assertEqual(result["error"], "APIisNotAvailable")
