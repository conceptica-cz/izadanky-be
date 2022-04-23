from unittest.mock import Mock, patch

from celery import states
from celery.result import AsyncResult
from django.urls import reverse
from rest_framework.test import APITestCase

from factories.users import UserFactory


class TaskViewTest(APITestCase):
    def setUp(self):
        self.user = UserFactory()

    @patch("common.views.AsyncResult")
    def test_get_task__started(self, mocked_async_result):
        mocked_result = Mock(spec=AsyncResult, state=states.STARTED, result={"pid": 42})
        mocked_async_result.return_value = mocked_result
        self.client.force_login(user=self.user)

        response = self.client.get(reverse("common:task", kwargs={"task_id": 1}))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["state"], states.STARTED)
        self.assertEqual(response.data["result"], None)

    @patch("common.views.AsyncResult")
    def test_get_task__pending(self, mocked_async_result):
        """Test that a pending task is returned as not found"""
        mocked_result = Mock(spec=AsyncResult, state=states.PENDING)
        mocked_async_result.return_value = mocked_result
        self.client.force_login(user=self.user)

        response = self.client.get(reverse("common:task", kwargs={"task_id": 1}))

        self.assertEqual(response.status_code, 404)

    @patch("common.views.AsyncResult")
    def test_get_task__success(self, mocked_async_result):
        mocked_result = Mock(
            spec=AsyncResult,
            state=states.SUCCESS,
            result=42,
        )
        mocked_async_result.return_value = mocked_result
        self.client.force_login(user=self.user)

        response = self.client.get(reverse("common:task", kwargs={"task_id": 1}))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["state"], states.SUCCESS)
        self.assertEqual(response.data["result"], 42)
