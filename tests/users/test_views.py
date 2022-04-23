from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from factories.references.persons import PersonFactory
from factories.users import UserFactory


class UserViewTest(APITestCase):
    def setUp(self) -> None:

        self.user = UserFactory(username="b0001")
        self.person = PersonFactory(person_number="0001")

    def test_get_unauthorized(self):
        response = self.client.get(reverse("users:user"))

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get(self):
        self.client.force_login(user=self.user)
        response = self.client.get(reverse("users:user"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data["username"], self.user.username)
        self.assertEqual(response.data["person"], self.person.id)
