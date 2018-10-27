from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q

from meetingroom.models import Room


class ScheduleItem(models.Model):
    title = models.CharField(max_length=280)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    start = models.DateTimeField()
    end = models.DateTimeField()
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-start',)

    def __repr__(self):
        date_time_pattern = '%Y-%m-%d %H:%M'
        return '<ScheduleItem: {}: ({} - {})>'.format(
            self.room.name,
            self.start.strftime(date_time_pattern),
            self.end.strftime(date_time_pattern),
        )

    def save(self, *args, **kwargs):
        edit = self._is_editing()
        if not self._room_available(edit):
            raise ValidationError(
                message='The room is already booked in this period.',
                code='conflict'
            )
        super().save(*args, **kwargs)

    def _is_editing(self):
        return bool(self.id)

    def _room_available(self, edit=False):
        schedule_items = self.__class__.objects.filter(
            Q(start=self.start) & Q(end=self.end) |
            Q(start__gte=self.start) & Q(start__lt=self.end) |
            Q(end__lte=self.end) & Q(end__gt=self.start),
            room=self.room
        )
        if edit:
            schedule_items = schedule_items.exclude(id=self.id)
        return not schedule_items.exists()
