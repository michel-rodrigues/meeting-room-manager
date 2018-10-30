from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView

from .models import Room
from .serializers import RoomSerializer


class CreateRoomAPIView(CreateAPIView):
    serializer_class = RoomSerializer
    http_method_names = [u'post']


class RetrieveUpdateDestroyRoomAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = RoomSerializer
    http_method_names = [u'get', u'put', u'delete']
    queryset = Room.objects.all()
