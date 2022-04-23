from django.urls import reverse
from requisitions.models.requisitions import Requisition
from requisitions.serializers.requisitions import RequisitionNestedSerializer
from rest_framework import status
from rest_framework.test import APITestCase

from factories.references.persons import PersonFactory
from factories.requisitions import RequisitionFactory
from factories.requisitions.patients import PatientFactory
from factories.users.models import UserFactory


class GetAllRequisitionsTest(APITestCase):
    def setUp(self) -> None:
        self.user = UserFactory()
        self.requisition_1 = RequisitionFactory()
        self.requisition_2 = RequisitionFactory()

    def test_get_all_requisitions(self):
        self.client.force_login(user=self.user)
        response = self.client.get(reverse("requisitions:requisition_list"))
        requisitions = Requisition.objects.all()
        serializer = RequisitionNestedSerializer(requisitions, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"], serializer.data)


class CreateRequisitionTest(APITestCase):
    def setUp(self) -> None:
        self.user = UserFactory()

    def test_new_requisition(self):
        patient = PatientFactory()
        applicant = PersonFactory()
        requisition_data = {
            "patient": patient.id,
            "text": "Test",
            "applicant": applicant.id,
        }
        self.client.force_login(user=self.user)
        response = self.client.post(
            reverse("requisitions:requisition_list"), data=requisition_data
        )
        self.assertEqual(
            response.status_code, status.HTTP_201_CREATED, msg=response.data
        )

        requisition = Requisition.objects.get(id=response.data["id"])
        self.assertEqual(requisition.patient, patient)
        self.assertEqual(requisition.applicant, applicant)
        self.assertEqual(requisition.text, "Test")
        self.assertEqual(requisition.created_by, self.user)


class GetSingleRequisitionTest(APITestCase):
    def setUp(self) -> None:
        self.user = UserFactory()
        self.requisition = RequisitionFactory()

    def test_get_single_requisition(self):
        self.client.force_login(user=self.user)
        response = self.client.get(
            reverse(
                "requisitions:requisition_detail", kwargs={"pk": self.requisition.pk}
            )
        )
        serializer = RequisitionNestedSerializer(self.requisition)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_get_single_requisition_not_found(self):
        self.client.force_login(user=self.user)
        response = self.client.get(
            reverse(
                "requisitions:requisition_detail",
                kwargs={"pk": self.requisition.pk + 1},
            )
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


# TODO: Test for update and delete
