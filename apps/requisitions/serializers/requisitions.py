from typing import Sequence

from django.db.models import QuerySet
from references.serializers import PersonSerializer
from rest_framework import serializers
from rest_framework.fields import empty

from ..models.requisitions import Requisition
from .patients import PatientSerializer

COMMON_FIELDS = {
    "id",
    "type",
    "suptype",
    "state",
    "text",
    "applicant",
    "solver",
    "created_at",
    "updated_at",
    "is_synced",
    "synced_at",
}

FIELDS_BY_TYPE = {
    Requisition.TYPE_IPHARM: {
        "patient": {"required": True},
        "file": {},
        "clinic": {"required": True},
        "diagnosis": {"required": True},
    },
    Requisition.TYPE_DELIVERY: {},
}


class RequisitionSerializer(serializers.ModelSerializer):
    def __init__(self, instance=None, data=empty, **kwargs):
        super().__init__(instance, data, **kwargs)
        if data != empty:
            additional_fields = FIELDS_BY_TYPE.get(data.get("type"), ())
            for field in additional_fields:
                if additional_fields[field].get("required"):
                    self.fields[field].required = True

    def to_representation(self, instance):
        data = super().to_representation(instance)
        additional_fields = set(FIELDS_BY_TYPE.get(instance.type, ()))
        fields_to_remove = set(data) - COMMON_FIELDS - additional_fields
        for field in fields_to_remove:
            data.pop(field)
        return data

    class Meta:
        model = Requisition
        exclude = ("is_deleted",)
        read_only_fields = ["id", "created_at", "updated_at"]


class RequisitionNestedSerializer(RequisitionSerializer):
    patient = PatientSerializer(read_only=True)
    applicant = PersonSerializer(read_only=True)
    solver = PersonSerializer(read_only=True)
