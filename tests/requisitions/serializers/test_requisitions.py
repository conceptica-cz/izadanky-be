from django.test import TestCase
from references.serializers import PersonSerializer
from requisitions.models import Requisition
from requisitions.serializers.requisitions import (
    RequisitionNestedSerializer,
    RequisitionSerializer,
)

from factories.references import PersonFactory
from factories.requisitions import PatientFactory, RequisitionFactory


class RequisitionSerializerTestCase(TestCase):
    def test_delivery_requisition_does_not_have_patient(self):
        requisition = RequisitionFactory(type=Requisition.TYPE_DELIVERY)
        serializer = RequisitionSerializer(requisition)
        self.assertNotIn("patient", serializer.data)

    def test_ipharm_requisition_does_have_patient(self):
        requisition = RequisitionFactory(type=Requisition.TYPE_IPHARM)
        serializer = RequisitionSerializer(requisition)
        self.assertIn("patient", serializer.data)

    def test_create_deliver_requisition(self):
        data = {
            "type": Requisition.TYPE_DELIVERY,
            "applicant": PersonFactory().id,
        }
        serializer = RequisitionSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        requisition = serializer.save()
        self.assertEqual(requisition.type, Requisition.TYPE_DELIVERY)

    def test_create_deliver_requisition(self):
        data = {
            "type": Requisition.TYPE_IPHARM,
            "patient": PatientFactory().id,
            "applicant": PersonFactory().id,
        }
        serializer = RequisitionSerializer(data=data)
        self.assertTrue(serializer.is_valid(), msg=serializer.errors)
        requisition = serializer.save()
        requisition = Requisition.objects.get(id=requisition.id)
        self.assertEqual(requisition.type, Requisition.TYPE_IPHARM)
        self.assertEqual(requisition.patient.id, data["patient"])

    def test_create_deliver_requisition_without_patient(self):
        data = {
            "type": Requisition.TYPE_IPHARM,
            "applicant": PersonFactory().id,
        }
        serializer = RequisitionSerializer(data=data)
        self.assertFalse(serializer.is_valid())


class RequisitionNestedSerializerTestCase(TestCase):
    def test_applicant_is_nested(self):
        requisition = RequisitionFactory()

        serializer = RequisitionNestedSerializer(instance=requisition)
        applicant_serializer = PersonSerializer(instance=requisition.applicant)

        self.assertEqual(
            serializer.data["applicant"],
            applicant_serializer.data,
        )
