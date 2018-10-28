from rest_framework import serializers
from rest_framework.serializers import ValidationError

from commons.exceptions import ScheduleConflict

from .models import ScheduleItem


class ScheduleItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = ScheduleItem
        fields = ('title', 'room', 'start', 'end')

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
