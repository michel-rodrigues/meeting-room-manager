from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView

from .models import Room
from .serializers import RoomSerializer


class CreateRoomAPIView(CreateAPIView):
    serializer_class = RoomSerializer
    http_method_names = [u'post']


class UpdateDestroyRoomAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = RoomSerializer
    http_method_names = [u'put', u'delete']
    queryset = Room.objects.all()
