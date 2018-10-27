from rest_framework.generics import ListCreateAPIView

from .models import ScheduleItem
from .serializers import ScheduleItemSerializer


class ListCreateScheduleItemAPIView(ListCreateAPIView):
    serializer_class = ScheduleItemSerializer
    http_method_names = [u'get', u'post']
    queryset = ScheduleItem.objects.all()
