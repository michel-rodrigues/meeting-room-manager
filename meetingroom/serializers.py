from rest_framework import serializers

from .models import Room


class RoomSerializer(serializers.ModelSerializer):

    class Meta:
        model = Room
        fields = ('pk', 'name')
        extra_kwargs = {'pk': {'read_only': True}}
