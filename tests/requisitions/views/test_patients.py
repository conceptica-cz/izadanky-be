import factory
from django.urls import reverse
from requisitions.filters import RequisitionFilter
from requisitions.models.requisitions import Requisition
from requisitions.serializers.requisitions import RequisitionSerializer
from rest_framework import status
from rest_framework.test import APITestCase

from factories.references.clinics import ClinicFactory
from factories.requisitions import RequisitionFactory
from factories.users.models import UserFactory


class GetAllRequisitionsTest(APITestCase):
    def setUp(self) -> None:
        self.user = UserFactory()
        self.requisition_1 = RequisitionFactory()
        self.requisition_2 = RequisitionFactory()

    def test_get_all_requisitions(self):
        self.client.force_login(user=self.user)
        response = self.client.get(reverse("requisition_list"))
        requisitions = Requisition.objects.all()
        serializer = RequisitionSerializer(requisitions, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"], serializer.data)


class CreateRequisitionTest(APITestCase):
    def setUp(self) -> None:
        self.user = UserFactory()

    def test_new_requisition_ambulance(self):
        requisition_data = factory.build(dict, FACTORY_CLASS=RequisitionFactory)
        self.client.force_login(user=self.user)
        response = self.client.post(reverse("requisition_list"), data=requisition_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class GetSingleRequisitionTest(APITestCase):
    def setUp(self) -> None:
        self.user = UserFactory()
        self.requisition = RequisitionFactory()

    def test_get_single_requisition(self):
        self.client.force_login(user=self.user)
        response = self.client.get(
            reverse("requisition_detail", kwargs={"pk": self.requisition.pk})
        )
        serializer = RequisitionSerializer(self.requisition)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_get_single_requisition_not_found(self):
        self.client.force_login(user=self.user)
        response = self.client.get(
            reverse("requisition_detail", kwargs={"pk": self.requisition.pk + 1})
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


# TODO: Test for update and delete
