from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)

from .models import Room
from .serializers import RoomSerializer


class ListCreateRoomAPIView(ListCreateAPIView):
    serializer_class = RoomSerializer
    http_method_names = [u'get', u'post']


class RetrieveUpdateDestroyRoomAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = RoomSerializer
    http_method_names = [u'get', u'put', u'delete']
    queryset = Room.objects.all()
