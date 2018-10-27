from django.db import models

from meetingroom.models import Room


class ScheduleItem(models.Model):
    title = models.CharField(max_length=280)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    start = models.DateTimeField()
    end = models.DateTimeField()

    class Meta:
        ordering = ('-start',)
