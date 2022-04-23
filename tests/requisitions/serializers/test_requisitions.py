from django.test import TestCase
from references.serializers import PersonSerializer
from requisitions.serializers.requisitions import RequisitionNestedSerializer

from factories.requisitions import RequisitionFactory


class RequisitionNestedSerializerTestCase(TestCase):
    def test_applicant_is_nested(self):
        requisition = RequisitionFactory()

        serializer = RequisitionNestedSerializer(instance=requisition)
        applicant_serializer = PersonSerializer(instance=requisition.applicant)

        self.assertEqual(
            serializer.data["applicant"],
            applicant_serializer.data,
        )
