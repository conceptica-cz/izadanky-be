from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics
from rest_framework.permissions import SAFE_METHODS

from ..filters import RequisitionFilter
from ..models.requisitions import Requisition
from ..serializers.requisitions import RequisitionSerializer
from .common import HistoryView


class RequisitionListView(generics.ListCreateAPIView):
    queryset = Requisition.objects.all()

    serializer_class = RequisitionSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = RequisitionFilter


class RequisitionDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Requisition.objects.all()
    serializer_class = RequisitionSerializer


class RequisitionHistoryView(HistoryView):
    queryset = Requisition.objects.all()
