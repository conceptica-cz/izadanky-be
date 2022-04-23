import factory
from faker import Faker


class PatientFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "requisitions.Patient"
        django_get_or_create = ["birth_number"]

    class Params:
        birth_date = factory.Faker("date_time_this_century")

    @factory.lazy_attribute
    def birth_number(self):
        birth = self.birth_date.strftime("%y%m%d")
        return f"{birth}{Faker().pyint(1000, 9999)}"

    external_id = factory.Sequence(lambda n: n)

    first_name = factory.Faker("first_name_male", locale="cs")
    last_name = factory.Faker("last_name_male", locale="cs")
    name = factory.LazyAttribute(lambda obj: f"{obj.first_name} {obj.last_name}")
