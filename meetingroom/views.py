from rest_framework.generics import CreateAPIView
from .serializers import RoomSerializer


class CreateRoomAPIView(CreateAPIView):
    serializer_class = RoomSerializer
    http_method_names = [u'post']
