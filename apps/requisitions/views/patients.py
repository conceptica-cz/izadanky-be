from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import (
    OpenApiParameter,
    extend_schema,
    extend_schema_view,
    inline_serializer,
)
from requisitions.models import Patient
from requisitions.serializers.patients import PatientSerializer
from requisitions.tasks import load_patient_task
from requisitions.views.common import HistoryView
from rest_framework import serializers, status
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.views import APIView


class PatientListView(ListAPIView):
    """
    Get all patients.
    """

    queryset = Patient.objects.all()
    serializer_class = PatientSerializer


class PatientDetailView(RetrieveAPIView):
    """
    Get patient.
    """

    queryset = Patient.objects.all()
    serializer_class = PatientSerializer


class PatientHistoryView(HistoryView):
    queryset = Patient.objects.all()


@extend_schema_view(
    post=extend_schema(
        parameters=[
            OpenApiParameter(
                name="birth_number",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description="The birth number of the patient to be found",
            ),
        ],
        responses={
            status.HTTP_202_ACCEPTED: inline_serializer(
                name="task_id",
                fields={"task_id": serializers.CharField()},
            )
        },
    ),
)
class PatientLoadView(APIView):
    """
    Start a long-running background task of getting the patient via 3rd-party API.

    One and only one of the following parameters must be provided: `birth_number`.

    To check the status of the task, use the `/tasks/<task_id>/` endpoint.

    The endpoint returns only the `task_id`. To get the result of the task, use
    the `/tasks/<task_id>/` endpoint. The result will be returned by
    the `/tasks/<task_id>/` endpoint in the result field.

    If patient is found by 3rd-party API, `Patient` instance will be created or got
    and the result will be dictionary like this::

        {
            "success": True,
            "data": {...} # patient serialized data,
        }

    If patent not found, the result will be dictionary like this::

        {
            "success": False,
            "error": "PatientNotFound"
        }

    If API is not available, the result will be dictionary like this::

        {
            "success": False,
            "error": "APIisNotAvailable"
        }

    If API returns error, the result will be dictionary like this::

        {
            "success": False,
            "error": "APIError"
        }

    """

    def post(self, request, *args, **kwargs):
        birth_number = request.query_params.get("birth_number")
        if birth_number is None:
            return Response(
                data={"error": "birth_number must be set"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        result = load_patient_task.delay(birth_number=birth_number)

        return Response(
            data={"task_id": result.task_id}, status=status.HTTP_202_ACCEPTED
        )
