from requisitions.models import Patient
from rest_framework import serializers


class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = read_only_fields = (
            "id",
            "birth_number",
            "external_id",
            "name",
            "first_name",
            "last_name",
        )
