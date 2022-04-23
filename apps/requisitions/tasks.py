import logging

from celery import shared_task
from requisitions.loaders.patient import load_patient

log = logging.getLogger(__name__)


@shared_task(
    ignore_result=False,
)
def load_patient_task(birth_number: str) -> dict:
    log.debug(
        "Loading patient",
        extra={"birth_number": birth_number},
    )
    result = load_patient(birth_number=birth_number)
    log.debug(
        "Finish loading patient",
        extra={"birth_number": birth_number, "result": result},
    )
    return result
