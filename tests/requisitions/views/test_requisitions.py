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
            "type:": Requisition.TYPE_IPHARM,
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
        self.assertEqual(requisition.is_synced, False)
        self.assertEqual(requisition.synced_at, None)


class GetSingleRequisitionTest(APITestCase):
    def setUp(self) -> None:
        self.user = UserFactory(is_app=False)
        self.requisition = RequisitionFactory(is_synced=True)

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


class UpdateRequisitionTest(APITestCase):
    def setUp(self) -> None:
        self.user = UserFactory(is_app=False)
        self.app_user = UserFactory(is_app=True)
        self.requisition = RequisitionFactory(is_synced=True, text="old text")

    def test_update_requisition(self):
        self.client.force_login(user=self.user)
        response = self.client.patch(
            reverse(
                "requisitions:requisition_detail", kwargs={"pk": self.requisition.pk}
            ),
            data={"text": "new text"},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        requisition = Requisition.objects.get(id=self.requisition.id)
        self.assertEqual(requisition.text, "new text")

    def test_update_requisition_is_synced_is_false_for_casual_user(self):
        self.client.force_login(user=self.user)
        response = self.client.patch(
            reverse(
                "requisitions:requisition_detail", kwargs={"pk": self.requisition.pk}
            ),
            data={"text": "new text"},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        requisition = Requisition.objects.get(id=self.requisition.id)
        self.assertEqual(requisition.is_synced, False)

    def test_update_requisition_is_synced_is_true_for_app_user(self):
        self.requisition.is_synced = False
        self.requisition.save()

        self.client.force_login(user=self.app_user)
        response = self.client.patch(
            reverse(
                "requisitions:requisition_detail", kwargs={"pk": self.requisition.pk}
            ),
            data={"text": "new text"},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        requisition = Requisition.objects.get(id=self.requisition.id)
        self.assertEqual(requisition.is_synced, True)
