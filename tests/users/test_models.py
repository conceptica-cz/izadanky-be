from django.test import TestCase

from factories.references import PersonFactory
from factories.users import UserFactory


class UserTest(TestCase):
    def setUp(self):
        self.person_001 = PersonFactory(person_number="001")
        self.person_002 = PersonFactory(person_number="002")
        self.person_003 = PersonFactory(person_number="003")

    def test_get_person_bxxx(self):
        user = UserFactory(username="b002")

        self.assertEqual(user.get_person(), self.person_002)

    def test_get_person_baxxx(self):
        user = UserFactory(username="ba003")

        self.assertEqual(user.get_person(), self.person_003)

    def test_get_person_non_existing(self):
        user = UserFactory(username="b004")

        self.assertEqual(user.get_person(), None)

    def test_get_person_invalid_username(self):
        user = UserFactory(username="username")

        self.assertEqual(user.get_person(), None)
