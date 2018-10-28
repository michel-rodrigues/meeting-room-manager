from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from .models import ScheduleItem
from .serializers import ScheduleItemSerializer, ScheduleItemListSerializer


class ListCreateScheduleItemAPIView(ListCreateAPIView):
    serializer_class = ScheduleItemSerializer
    list_serializer_class = ScheduleItemListSerializer
    http_method_names = [u'get', u'post']
    queryset = ScheduleItem.objects.all().select_related('room')

    def list(self, request, *args, **kwargs):
        self.serializer_class = self.list_serializer_class
        return super().list(request, *args, **kwargs)


class UpdateDestroyScheduleItemAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = ScheduleItemSerializer
    http_method_names = [u'put', u'delete']
    queryset = ScheduleItem.objects.all()
