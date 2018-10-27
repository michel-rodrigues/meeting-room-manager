from rest_framework import serializers
from rest_framework.serializers import ValidationError

from meetingroom.models import Room

from .models import ScheduleItem


class ScheduleItemSerializer(serializers.ModelSerializer):

    room = serializers.SlugField(max_length=150)

    class Meta:
        model = ScheduleItem
        fields = ('title', 'room', 'start', 'end')

    def validate_room(self, value):
        try:
            room = Room.objects.get(slug=value)
        except Room.DoesNotExist:
            raise ValidationError(
                detail=["Room doesn't exist"],
                code='required',
            )
        else:
            return room
