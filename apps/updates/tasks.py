import logging

from celery import shared_task
from updates.models import Source

from izadanky_web.settings import DEFAULT_RETRY_DELAY

logger = logging.getLogger(__name__)


@shared_task(
    bind=True,
    ignore_result=True,
    max_retries=1,
    default_retry_delay=DEFAULT_RETRY_DELAY,
)
def update(self, source_name: str, full_update=False, **kwargs):
    logger.info("Task update has been started. task_id: %s", self.request.id)
    source = Source.objects.get_or_create_from_settings(name=source_name)
    source.update(full_update=full_update, **kwargs)
