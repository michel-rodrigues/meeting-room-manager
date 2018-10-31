import logging
from rest_framework import serializers
from django.utils import timezone

from meetingroom.serializers import RoomSerializer
from .models import ScheduleItem


logger = logging.getLogger('schedule.serializers')


class ScheduleItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = ScheduleItem
        fields = ('pk', 'title', 'room', 'start', 'end')
        extra_kwargs = {'pk': {'read_only': True}}

    def create(self, validated_data):
        try:
            return super().create(validated_data)
        except:
            pattern = "Creating schedule item - {timestamp} - data:{data}"
            msg = pattern.format(timestamp=timezone.now(), data=validated_data)
            logger.exception(msg)
            raise

    def update(self, instance, validated_data):
        try:
            return super().update(instance, validated_data)
        except:
            pattern = "Updating schedule item - {timestamp} - data:{data}"
            msg = pattern.format(timestamp=timezone.now(), data=validated_data)
            logger.exception(msg)
            raise


class ScheduleItemListSerializer(ScheduleItemSerializer):
    room = RoomSerializer(read_only=True)
