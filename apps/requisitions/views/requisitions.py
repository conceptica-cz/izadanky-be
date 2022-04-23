from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics

from ..filters import RequisitionFilter
from ..models.requisitions import Requisition
from ..serializers.requisitions import (
    RequisitionNestedSerializer,
    RequisitionSerializer,
)
from .common import HistoryView


class RequisitionListView(generics.ListCreateAPIView):
    queryset = (
        Requisition.objects.select_related("patient")
        .select_related("created_by")
        .select_related("applicant")
        .all()
    )

    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = RequisitionFilter

    def get_serializer_class(self):
        if self.request.method == "GET":
            return RequisitionNestedSerializer
        return RequisitionSerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class RequisitionDetailView(generics.RetrieveUpdateAPIView):
    queryset = Requisition.objects.all()

    def get_serializer_class(self):
        if self.request.method == "GET":
            return RequisitionNestedSerializer
        return RequisitionSerializer


class RequisitionHistoryView(HistoryView):
    queryset = Requisition.objects.all()
