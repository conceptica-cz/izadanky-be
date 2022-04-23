from unittest import TestCase
from unittest.mock import Mock, patch

from requisitions.loaders.ipharm_patient import load_ipahrm_patient
from requisitions.loaders.patient import APIError, PatientNotFound


@patch("requisitions.loaders.ipharm_patient.requests.get")
class GetPatientTest(TestCase):
    def test_get_patient_via_birth_number__valid(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": 1,
                    "some_data": "some_value",
                    "external_id": "59",
                    "name": "John Doe",
                    "first_name": "John",
                    "last_name": "Doe",
                    "birth_number": "5603201072",
                }
            ],
        }

        patient = load_ipahrm_patient("5603201072")

        self.assertEqual(patient.external_id, "59")
        self.assertEqual(patient.name, "John Doe")
        self.assertEqual(patient.first_name, "John")
        self.assertEqual(patient.last_name, "Doe")
        self.assertEqual(patient.birth_number, "5603201072")

    def test_get_patient_via_birth_number__patient_doesnt_exist(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [],
        }
        with self.assertRaises(PatientNotFound):
            load_ipahrm_patient("5603201072")

    def test_get_patient_via_birth_number__status_isnt_200(self, mock_get):
        mock_get.return_value.status_code = 400
        mock_get.return_value.json.return_value = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [],
        }
        with self.assertRaises(APIError):
            load_ipahrm_patient("5603201072")
