from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from .models import ScheduleItem
from .serializers import ScheduleItemSerializer


class ListCreateScheduleItemAPIView(ListCreateAPIView):
    serializer_class = ScheduleItemSerializer
    http_method_names = [u'get', u'post']
    queryset = ScheduleItem.objects.all()


class UpdateDestroyScheduleItemAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = ScheduleItemSerializer
    http_method_names = [u'put', u'delete']
    queryset = ScheduleItem.objects.all()

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        response.data['room'] = request.data['room']
        return response
