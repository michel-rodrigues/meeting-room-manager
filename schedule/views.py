from django_filters import rest_framework as filters
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from .filters import ScheduleItemFilter
from .models import ScheduleItem
from .serializers import ScheduleItemSerializer, ScheduleItemListSerializer


class ListCreateScheduleItemAPIView(ListCreateAPIView):
    serializer_class = ScheduleItemSerializer
    list_serializer_class = ScheduleItemListSerializer
    http_method_names = ['get', 'post']
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = ScheduleItemFilter
    queryset = ScheduleItem.objects.all().select_related('room')

    def list(self, request, *args, **kwargs):
        self.serializer_class = self.list_serializer_class
        return super().list(request, *args, **kwargs)


class RetrieveUpdateDestroyScheduleItemAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = ScheduleItemSerializer
    http_method_names = ['get', 'put', 'delete']
    queryset = ScheduleItem.objects.all()
