import logging

from django.db import models
from requisitions.managers.requisitions import RequisitionManager
from updates.models import BaseUpdatableModel

logger = logging.getLogger(__name__)


class Requisition(BaseUpdatableModel):
    STATE_CREATED = "created"
    STATE_SENT = "sent"
    STATE_CANCELED = "canceled"
    STATE_REFUSED = "refused"
    STATE_SOLVED = "solved"

    STATE_CHOICES = (
        (STATE_CREATED, "Created"),
        (STATE_SENT, "Sent"),
        (STATE_CANCELED, "Canceled"),
        (STATE_REFUSED, "Refused"),
        (STATE_SOLVED, "Solved"),
    )

    state = models.CharField(
        max_length=255, choices=STATE_CHOICES, default=STATE_CREATED
    )
    patient = models.ForeignKey("requisitions.Patient", on_delete=models.CASCADE)
    text = models.TextField(blank=True, null=True)
    file = models.FileField(upload_to="requisitions", blank=True, null=True)
    applicant = models.ForeignKey(
        "references.Person", on_delete=models.CASCADE, related_name="requisitions"
    )
    created_by = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="requisitions"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = RequisitionManager()
