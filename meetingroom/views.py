from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)

from .models import Room
from .serializers import RoomSerializer


class ListCreateRoomAPIView(ListCreateAPIView):
    serializer_class = RoomSerializer
    http_method_names = ['get', 'post']
    queryset = Room.objects.all()


class RetrieveUpdateDestroyRoomAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = RoomSerializer
    http_method_names = ['get', 'put', 'delete']
    queryset = Room.objects.all()
