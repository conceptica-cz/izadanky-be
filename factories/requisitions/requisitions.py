import factory
from requisitions.models.requisitions import Requisition


class RequisitionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Requisition

    patient = factory.SubFactory("factories.requisitions.patients.PatientFactory")
    text = factory.Faker("text")
    file = None
    applicant = factory.SubFactory("factories.references.persons.PersonFactory")
    created_by = factory.SubFactory("factories.users.models.UserFactory")
