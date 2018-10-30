from rest_framework import serializers
from rest_framework.serializers import ValidationError

from commons.exceptions import ScheduleConflict
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
        except ScheduleConflict as error:
            raise ValidationError(
                detail={'room': [error.message]},
                code=error.code,
            )

    def update(self, instance, validated_data):
        try:
            return super().update(instance, validated_data)
        except ScheduleConflict as error:
            raise ValidationError(
                detail={'room': [error.message]},
                code=error.code,
            )


class ScheduleItemListSerializer(ScheduleItemSerializer):
    room = RoomSerializer(read_only=True)
