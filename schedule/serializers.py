from rest_framework import serializers
from rest_framework.serializers import ValidationError

from commons.exceptions import ScheduleConflict
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
