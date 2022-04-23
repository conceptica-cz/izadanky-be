from celery.result import AsyncResult
from common.serializers import TaskSerializer
from common.tasks import Task, TaskDoesNotExist
from drf_spectacular.utils import extend_schema, extend_schema_view, inline_serializer
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView


@extend_schema_view(
    get=extend_schema(
        responses={
            status.HTTP_200_OK: inline_serializer(
                name="Task",
                fields={
                    "state": serializers.CharField(),
                    "result": serializers.DictField(),
                },
            ),
        },
    ),
)
class TaskView(APIView):
    def get(self, request, task_id):
        """
        Get task status and result.

        Field `state` corresponds to `celery.states`
        (see https://docs.celeryq.dev/en/stable/reference/celery.states.html).

        A status of `STARTED` means that the task has started.
        A status of `SUCCESS` means that the task has finished successfully.
        A status of `FAILURE` means that the task has failed.

        The response contains a field `result` only if the task
        has finished successfully.

        Field `result` depends on the task. Usually it is a dictionary.
        See the description of endpoint that initializes the task
        (e.g. `/api/v1/patients/load-patients/`).
        """
        async_result = AsyncResult(task_id)
        try:
            task_result = Task(async_result)
        except TaskDoesNotExist:
            return Response(data={"detail": "Task not found"}, status=404)
        serializer = TaskSerializer(task_result)
        return Response(serializer.data)
