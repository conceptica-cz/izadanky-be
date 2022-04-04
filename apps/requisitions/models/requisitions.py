import logging

from requisitions.managers.requisitions import RequisitionManager
from updates.models import BaseUpdatableModel

logger = logging.getLogger(__name__)


class Requisition(BaseUpdatableModel):
    objects = RequisitionManager()
