from datetime import timedelta

from django.test import TestCase
from django.utils import timezone

from meetingroom.models import Room
from ..exceptions import ScheduleConflict
from ..models import ScheduleItem


class ScheduleItemTest(TestCase):

    def setUp(self):
        self.room = Room.objects.create(name='Torre Stark')
        self.now = timezone.now()
        self.one_hour_later = self.now + timedelta(hours=1)
        self.schedule_item_1 = ScheduleItem.objects.create(
            title='Planning Novos Negócios',
            room=self.room,
            start=self.now,
            end=self.one_hour_later,
        )
        self.schedule_item_2 = ScheduleItem(
            title='Planning Logística',
            room=self.schedule_item_1.room,
        )

    def test_when_does_not_exist_other_item_with_exactly_the_same_room_and_period(self):  # noqa: E501
        self.schedule_item_2.start = self.now + timedelta(hours=2)
        self.schedule_item_2.end = self.one_hour_later + timedelta(hours=2)
        self.assertTrue(self.schedule_item_2._room_available())

    def test_when_exist_other_item_with_exactly_the_same_room_and_period(self):
        self.schedule_item_2.start = self.now
        self.schedule_item_2.end = self.one_hour_later
        self.assertFalse(self.schedule_item_2._room_available())
        with self.assertRaises(ScheduleConflict) as error:
            self.schedule_item_2.save()
        error_message = 'The room is already booked in this period.'
        self.assertEqual(str(error.exception.detail), error_message)
        self.assertEqual(error.exception.get_codes(), 'period_conflict')

    def test_when_other_item_has_field_start_within_item_period(self):
        self.schedule_item_2.start = self.now + timedelta(minutes=30)
        self.schedule_item_2.end = self.one_hour_later + timedelta(minutes=30)
        self.assertFalse(self.schedule_item_2._room_available())
        with self.assertRaises(ScheduleConflict) as error:
            self.schedule_item_2.save()
        error_message = 'The room is already booked in this period.'
        self.assertEqual(str(error.exception.detail), error_message)
        self.assertEqual(error.exception.get_codes(), 'period_conflict')

    def test_when_other_item_has_field_end_within_item_period(self):
        self.schedule_item_2.start = self.now - timedelta(minutes=30)
        self.schedule_item_2.end = self.one_hour_later - timedelta(minutes=30)
        self.assertFalse(self.schedule_item_2._room_available())
        with self.assertRaises(ScheduleConflict) as error:
            self.schedule_item_2.save()
        error_message = 'The room is already booked in this period.'
        self.assertEqual(str(error.exception.detail), error_message)
        self.assertEqual(error.exception.get_codes(), 'period_conflict')

    def test_when_the_period_begins_immediately_after_another_item(self):
        self.schedule_item_2.start = self.now + timedelta(hours=1)
        self.schedule_item_2.end = self.one_hour_later + timedelta(hours=1)
        self.assertTrue(self.schedule_item_2._room_available())

    def test_when_the_period_ends_immediately_before_another_item(self):
        self.schedule_item_2.start = self.now - timedelta(hours=1)
        self.schedule_item_2.end = self.one_hour_later - timedelta(hours=1)
        self.assertTrue(self.schedule_item_2._room_available())

    def test_can_edit_item_with_same_values(self):
        previous_update = self.schedule_item_1.updated_at
        self.schedule_item_1.save()
        last_update = self.schedule_item_1.updated_at
        self.assertGreater(last_update, previous_update)

    def test_when_set_field_start_greater_than_end(self):
        self.schedule_item_2.start = self.now + timedelta(minutes=1)
        self.schedule_item_2.end = self.now
        with self.assertRaises(ScheduleConflict) as error:
            self.schedule_item_2.save()
        error_message = 'Start date must begin before end date.'
        self.assertEqual(str(error.exception.detail), error_message)
        self.assertEqual(error.exception.get_codes(), 'inverted_date_values')
