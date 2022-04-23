from references.serializers import PersonSerializer
from rest_framework import serializers

from ..models.requisitions import Requisition
from .patients import PatientSerializer


class RequisitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Requisition
        exclude = ("is_deleted", "created_by")
        read_only_fields = ["id", "created_at", "updated_at"]


class RequisitionNestedSerializer(serializers.ModelSerializer):
    patient = PatientSerializer(read_only=True)
    applicant = PersonSerializer(read_only=True)

    class Meta:
        model = Requisition
        fields = (
            "id",
            "patient",
            "text",
            "file",
            "applicant",
            "created_at",
            "updated_at",
        )
        read_only_fields = ["id"]
