import random

from django.conf import settings
from django.core.management.base import BaseCommand

from factories.references import (
    AdverseEffectFactory,
    ExternalDepartmentFactory,
    IdentificationFactory,
    TagFactory,
)
from factories.requisitions import (
    CareFactory,
    CheckInFactory,
    PharmacologicalEvaluationFactory,
    PharmacologicalPlanCommentFactory,
    PharmacologicalPlanFactory,
    RequisitionInformationFactory,
    RiskDrugHistoryFactory,
)
from factories.users import UserFactory


class Command(BaseCommand):
    help = "Populate database with fake data"

    def handle(self, *args, **options):
        if settings.ENVIRONMENT not in ["test", "development", "local"]:
            self.stdout.write(
                self.style.ERROR(
                    "This command should only be used in test, local or development environments."
                )
            )
            return
        print("Populating database. Please wait...")

        users = [
            UserFactory(),
            UserFactory(),
            UserFactory(),
            UserFactory(),
            UserFactory(),
        ]

        for i in range(50):
            TagFactory()
            AdverseEffectFactory()
        for i in range(200):
            care = CareFactory()
            print(f"Requisition {care.requisition} created")
            if random.randint(0, 1):
                CheckInFactory(care=care)
                if random.randint(0, 1):
                    pharmacological_plan = PharmacologicalPlanFactory(care=care)
                    [
                        PharmacologicalPlanCommentFactory(
                            pharmacological_plan=pharmacological_plan,
                            comment_type="verification",
                        )
                        for _ in range(random.randint(0, 2))
                    ]
                    [
                        PharmacologicalPlanCommentFactory(
                            pharmacological_plan=pharmacological_plan,
                            comment_type="comment",
                        )
                        for _ in range(random.randint(0, 5))
                    ]
                    RiskDrugHistoryFactory(care=care)
                    for _ in range(random.randint(1, 4)):
                        requisition_information = RequisitionInformationFactory(
                            care=care
                        )
                        for i in range(random.randint(1, 4)):
                            requisition_information.text = i
                            requisition_information.save()
                            requisition_information.set_history_user(
                                random.choice(users)
                            )

                    [
                        PharmacologicalEvaluationFactory(care=care)
                        for _ in range(random.randint(1, 5))
                    ]

        for i in range(30):
            ExternalDepartmentFactory()
        IdentificationFactory()
        print("Database was populated.")
