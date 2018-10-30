from rest_framework import serializers

from meetingroom.serializers import RoomSerializer
from .models import ScheduleItem


class ScheduleItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = ScheduleItem
        fields = ('pk', 'title', 'room', 'start', 'end')
        extra_kwargs = {'pk': {'read_only': True}}

    def create(self, validated_data):
        try:
            return super().create(validated_data)
        except:
            raise

    def update(self, instance, validated_data):
        try:
            return super().update(instance, validated_data)
        except:
            raise


class ScheduleItemListSerializer(ScheduleItemSerializer):
    room = RoomSerializer(read_only=True)
