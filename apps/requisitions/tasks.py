import logging

from celery import shared_task
from requisitions.loaders.patient import load_patient

log = logging.getLogger(__name__)


@shared_task(
    ignore_result=False,
)
def load_patient_task(birth_number: str = None, external_id: str = None) -> dict:
    log.debug(
        "Loading patient",
        extra={"birth_number": birth_number, "external_id": external_id},
    )
    result = load_patient(birth_number=birth_number, external_id=external_id)
    log.debug(
        "Finish loading patient",
        extra={
            "birth_number": birth_number,
            "external_id": external_id,
            "result": result,
        },
    )
    return result
