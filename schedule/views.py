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

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        room = {
            'title': self.instance.room.name,
            'slug': self.instance.room.slug,
        }
        response.data['room'] = room
        return response

    def perform_create(self, serializer):
        self.instance = serializer.save()


class UpdateDestroyScheduleItemAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = ScheduleItemSerializer
    http_method_names = [u'put', u'delete']
    queryset = ScheduleItem.objects.all()

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        room = {
            'title': self.instance.room.name,
            'slug': self.instance.room.slug,
        }
        response.data['room'] = room
        return response

    def perform_update(self, serializer):
        self.instance = serializer.save()
