import logging

import requests
from django.conf import settings
from requisitions.loaders.patient import (
    APIError,
    APIisNotAvailable,
    Patient,
    PatientNotFound,
)

logger = logging.getLogger(__name__)


def load_ipharm_patient(birth_number=None, external_id=None):
    """
    Load patient via iPharm API

    :param birth_number: patient's birth number
    :return:
    """
    if birth_number is None and external_id is None:
        raise ValueError("Either birth_number or extrenal_id must be provided")
    if birth_number is not None:
        url = f"{settings.BASE_IPHARM_URL }/patients/?birth_number={birth_number}"
    else:
        url = f"{settings.BASE_IPHARM_URL }/patients/?external_id={external_id}"
    headers = {"Authorization": f"Bearer {settings.IPHARM_TOKEN}"}
    timeout = settings.IPHARM_TIMEOUT
    try:
        logger.debug(f"Requesting ipharm patient", extra={"url": url})
        response = requests.get(url, headers=headers, timeout=timeout)
    except requests.exceptions.RequestException as e:
        logger.error(
            f"Error requesting ipharm patient", extra={"url": url, "exception": e}
        )
        raise APIisNotAvailable(e)

    if response.status_code != 200:
        logger.error(
            f"Error requesting ipharm patient",
            extra={
                "url": url,
                "status_code": response.status_code,
                "text": response.text,
            },
        )
        raise APIError(response.status_code, response.text)
    data = response.json()

    if not data["results"]:
        raise PatientNotFound(birth_number)
    else:
        patient_data = data["results"][0]
        patient = Patient(
            birth_number=patient_data["birth_number"],
            external_id=patient_data["external_id"],
            name=patient_data["name"],
            first_name=patient_data["first_name"],
            last_name=patient_data["last_name"],
        )
        return patient
