from dataclasses import dataclass

from common.utils import get_func_from_path
from django.conf import settings
from requisitions.models.patients import Patient as PatientModel
from requisitions.serializers.patients import PatientSerializer


class PatientNotFound(Exception):
    pass


class APIisNotAvailable(Exception):
    pass


class APIError(Exception):
    pass


@dataclass
class Patient:
    """
    Patient class
    """

    birth_number: str
    external_id: str
    name: str
    first_name: str
    last_name: str


def load_patient(birth_number=None, external_id=None) -> dict:
    """
    Get patient from third party API.

    If patient is found, gets or creates Patient instance and returns dictionary like this::

        {
            "success": True,
            "data": {...} # patient serialized data,
        }

    If patent not found, returns dictionary like this::

        {
            "success": False,
            "error": "PatientNotFound"
        }

    If API is not available, returns dictionary like this::

        {
            "success": False,
            "error": "APIisNotAvailable"
        }

    If API returns error, returns dictionary like this::

        {
            "success": False,
            "error": "APIError"
        }


    :param birth_number: the patient's birth number.
    :return: dictionary with patient data or error description.
    """
    if birth_number is None and external_id is None:
        raise ValueError("Either birth_number or external_id must be provided")
    try:
        if birth_number is not None:
            patient_model = PatientModel.objects.get(birth_number=birth_number)
        else:
            patient_model = PatientModel.objects.get(external_id=external_id)
    except PatientModel.DoesNotExist:
        pass
    else:
        data = PatientSerializer(patient_model).data
        return {"success": True, "data": data}

    loader = get_func_from_path(settings.PATIENT_LOADER)
    try:
        patient = loader(birth_number=birth_number, external_id=external_id)
    except (PatientNotFound, APIError, APIisNotAvailable) as e:
        return {
            "success": False,
            "error": e.__class__.__name__,
        }
    patient_model = PatientModel.objects.create(
        birth_number=patient.birth_number,
        external_id=patient.external_id,
        name=patient.name,
        first_name=patient.first_name,
        last_name=patient.last_name,
    )
    data = PatientSerializer(patient_model).data
    return {"success": True, "data": data}
