from unittest.mock import Mock, patch

from django.test import override_settings
from django.urls import reverse
from requisitions.models import Patient
from requisitions.serializers.patients import PatientSerializer
from rest_framework.test import APITestCase

from factories.requisitions import PatientFactory
from factories.users import UserFactory


class TestPatients(APITestCase):
    def setUp(self):
        """
        Set up the test
        """
        user = UserFactory()
        self.client.force_login(user)
        self.patient_1 = PatientFactory()
        self.patient_2 = PatientFactory()
        self.patient_3 = PatientFactory()

    def test_get_patients(self):
        """
        Test that we can get all patients
        """
        response = self.client.get("/api/v1/patients/")

        self.assertEqual(response.status_code, 200)

        expected_results = PatientSerializer(
            instance=Patient.objects.all(), many=True
        ).data

        self.assertEqual(response.data["results"], expected_results)

    def test_get_patient(self):
        """
        Test that we can get a patient
        """
        response = self.client.get(
            reverse("requisitions:patient_detail", kwargs={"pk": self.patient_1.id})
        )
        self.assertEqual(response.status_code, 200)
        expected_data = PatientSerializer(instance=self.patient_1).data
        self.assertEqual(response.data, expected_data)

    @patch("requisitions.views.patients.load_patient_task.delay")
    def test_load_patient(self, mock_load_patient_task):
        mock_load_patient_task.return_value = Mock(task_id="123")
        response = self.client.post("/api/v1/patients/load-patient/?birth_number=42")
        self.assertEqual(response.status_code, 202)
        mock_load_patient_task.assert_called_with(birth_number="42")

    def test_load_patient_return_400_if_birth_number_missing(self):
        response = self.client.post("/api/v1/patients/load-patient/")
        self.assertEqual(response.status_code, 400)
