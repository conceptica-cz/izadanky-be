from rest_framework import serializers

from ..models.requisitions import Requisition


class RequisitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Requisition
        exclude = ["is_deleted"]
        read_only_fields = ["id"]
