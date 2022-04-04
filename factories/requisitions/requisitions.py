import factory
from factory import fuzzy
from faker import Faker
from requisitions.models.requisitions import Requisition


class RequisitionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Requisition
        django_get_or_create = ["id"]

    id = factory.Sequence(lambda n: n)
