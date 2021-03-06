import factory
from requisitions.models.requisitions import Requisition


class RequisitionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Requisition

    type = Requisition.TYPE_IPHARM
    subtype = Requisition.SUBTYPE_IPHARM_CONCILATION
    patient = factory.SubFactory("factories.requisitions.patients.PatientFactory")
    clinic = factory.SubFactory("factories.references.clinics.ClinicFactory")
    diagnosis = factory.SubFactory("factories.references.diagnoses.DiagnosisFactory")
    text = factory.Faker("text")
    file = None
    applicant = factory.SubFactory("factories.references.persons.PersonFactory")
