from datetime import timedelta

from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone

from meetingroom.models import Room
from ..models import ScheduleItem


class ScheduleItemTest(TestCase):

    def setUp(self):
        self.room = Room.objects.create(name='Torre Stark', slug='torre-stark')
        self.now = timezone.now()
        self.one_hour_later = self.now + timedelta(hours=1)
        self.schedule_item = ScheduleItem.objects.create(
            title='Planning Novos Negócios',
            room=self.room,
            start=self.now,
            end=self.one_hour_later,
        )

    def test_when_does_not_exist_other_item_with_exactly_the_same_room_and_period(self):  # noqa: E501
        schedule_item = ScheduleItem(
            title='Planning Logística',
            room=self.schedule_item.room,
            start=self.schedule_item.start + timedelta(hours=2),
            end=self.schedule_item.end + timedelta(hours=2),
        )
        self.assertTrue(schedule_item._room_available())

    def test_when_exist_other_item_with_exactly_the_same_room_and_period(self):
        schedule_item = ScheduleItem(
            title='Planning Logística',
            room=self.schedule_item.room,
            start=self.schedule_item.start,
            end=self.schedule_item.end,
        )
        self.assertFalse(schedule_item._room_available())
        with self.assertRaises(ValidationError) as error:
            schedule_item.save()
        error_message = 'The room is already booked in this period.'
        self.assertEqual(error.exception.message, error_message)
        self.assertEqual(error.exception.code, 'conflict')

    def test_when_other_item_has_field_start_within_item_period(self):
        schedule_item = ScheduleItem(
            title='Planning Logística',
            room=self.schedule_item.room,
            start=self.schedule_item.start + timedelta(minutes=30),
            end=self.schedule_item.end + timedelta(minutes=30),
        )
        self.assertFalse(schedule_item._room_available())
        with self.assertRaises(ValidationError) as error:
            schedule_item.save()
        error_message = 'The room is already booked in this period.'
        self.assertEqual(error.exception.message, error_message)
        self.assertEqual(error.exception.code, 'conflict')

    def test_when_other_item_has_field_end_within_item_period(self):
        schedule_item = ScheduleItem(
            title='Planning Logística',
            room=self.schedule_item.room,
            start=self.schedule_item.start - timedelta(minutes=30),
            end=self.schedule_item.end - timedelta(minutes=30),
        )
        self.assertFalse(schedule_item._room_available())
        with self.assertRaises(ValidationError) as error:
            schedule_item.save()
        error_message = 'The room is already booked in this period.'
        self.assertEqual(error.exception.message, error_message)
        self.assertEqual(error.exception.code, 'conflict')

    def test_when_the_period_begins_immediately_after_another_item(self):
        schedule_item = ScheduleItem(
            title='Planning Logística',
            room=self.schedule_item.room,
            start=self.schedule_item.start + timedelta(hours=1),
            end=self.schedule_item.end + timedelta(hours=1),
        )
        self.assertTrue(schedule_item._room_available())
        previous_update = self.schedule_item.updated_at
        self.schedule_item.save()
        last_update = self.schedule_item.updated_at
        self.assertGreater(last_update, previous_update)

    def test_when_the_period_ends_immediately_before_another_item(self):
        schedule_item = ScheduleItem(
            title='Planning Logística',
            room=self.schedule_item.room,
            start=self.schedule_item.start - timedelta(hours=1),
            end=self.schedule_item.end - timedelta(hours=1),
        )
        self.assertTrue(schedule_item._room_available())
        previous_update = self.schedule_item.updated_at
        self.schedule_item.save()
        last_update = self.schedule_item.updated_at
        self.assertGreater(last_update, previous_update)

    def test_can_edit_item_with_same_values(self):
        previous_update = self.schedule_item.updated_at
        self.schedule_item.save()
        last_update = self.schedule_item.updated_at
        self.assertGreater(last_update, previous_update)
