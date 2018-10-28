from collections import OrderedDict
from datetime import timedelta

from django.urls import reverse
from django.utils import timezone

from rest_framework import status
from rest_framework.test import APITestCase, APIRequestFactory

from meetingroom.models import Room
from ..models import ScheduleItem
from ..views import (
    ListCreateScheduleItemAPIView,
    UpdateDestroyScheduleItemAPIView,
)


class ListCreateScheduleItemTest(APITestCase):

    def setUp(self):
        self.now = timezone.now()
        self.one_hour_later = self.now + timedelta(hours=1)
        self.view = ListCreateScheduleItemAPIView.as_view()
        self.factory = APIRequestFactory()
        self.url = reverse('meetingroom:schedule:list-create')
        self.room = Room.objects.create(
            name='Torre Stark',
            slug='torre-stark',
        )
        self.data = {
            'title': 'Planning Novos Negócios',
            'room': self.room.pk,
            'start': self.now,
            'end': self.one_hour_later,
        }

    def test_creating_item_schedule(self):
        request = self.factory.post(self.url, self.data, format='json')
        response = self.view(request).render()
        start = self.data['start'].isoformat()
        end = self.data['end'].isoformat()
        self.data['start'] = start.replace('+00:00', 'Z')
        self.data['end'] = end.replace('+00:00', 'Z')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, self.data)

    def test_fail_create_item_schedule_when_room_slug_is_missing(self):
        self.data.pop('room')
        request = self.factory.post(self.url, self.data, format='json')
        response = self.view(request).render()
        error_detail = response.data['room'][0]
        self.assertEqual(error_detail.code, 'required')
        self.assertEqual(str(error_detail), 'This field is required.')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_fail_create_item_schedule_when_room_does_not_exist(self):
        self.data['room'] = 2
        request = self.factory.post(self.url, self.data, format='json')
        response = self.view(request).render()
        error_detail = response.data['room'][0]
        self.assertEqual(error_detail.code, 'does_not_exist')
        self.assertEqual(
            str(error_detail),
            'Invalid pk "2" - object does not exist.'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_fail_create_item_schedule_when_there_are_period_conflict(self):
        self.schedule_item = ScheduleItem.objects.create(
            title='Planning Novos Negócios',
            room=self.room,
            start=self.now,
            end=self.one_hour_later,
        )
        self.data['start'] = self.now + timedelta(minutes=30)
        self.data['end'] = self.one_hour_later + timedelta(minutes=30)
        request = self.factory.post(self.url, self.data, format='json')
        response = self.view(request).render()
        error_detail = response.data['room'][0]
        error_message = 'The room is already booked in this period.'
        self.assertEqual(error_detail.code, 'conflict')
        self.assertEqual(str(error_detail), error_message)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_listing_all_items(self):
        schedule_item_1 = ScheduleItem.objects.create(
            title='Planning Novos Negócios',
            room=self.room,
            start=self.now,
            end=self.one_hour_later,
        )
        schedule_item_2 = ScheduleItem.objects.create(
            title='Planning Logística',
            room=self.room,
            start=self.now + timedelta(hours=1),
            end=self.one_hour_later + timedelta(hours=1),
        )
        room = OrderedDict(name=self.room.name, slug=self.room.slug)
        serialized_schedule_item_1 = OrderedDict(
            title=schedule_item_1.title,
            room=room,
            start=schedule_item_1.start.isoformat().replace('+00:00', 'Z'),
            end=schedule_item_1.end.isoformat().replace('+00:00', 'Z'),
        )
        serialized_schedule_item_2 = OrderedDict(
            title=schedule_item_2.title,
            room=room,
            start=schedule_item_2.start.isoformat().replace('+00:00', 'Z'),
            end=schedule_item_2.end.isoformat().replace('+00:00', 'Z'),
        )
        expected_data = [
            serialized_schedule_item_2,
            serialized_schedule_item_1,
        ]
        request = self.factory.get(self.url)
        response = self.view(request).render()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)


class UpdateDestroyRoomTest(APITestCase):

    def setUp(self):
        self.now = timezone.now()
        self.one_hour_later = self.now + timedelta(hours=1)
        self.view = UpdateDestroyScheduleItemAPIView.as_view()
        self.factory = APIRequestFactory()
        self.room = Room.objects.create(
            name='Torre Stark',
            slug='torre-stark',
        )
        self.data = {
            'title': 'Planning Novos Negócios',
            'room': self.room.pk,
            'start': self.now,
            'end': self.one_hour_later,
        }
        self.schedule_item = ScheduleItem.objects.create(
            title=self.data.get('title'),
            room=self.room,
            start=self.data.get('start'),
            end=self.data.get('end'),
        )
        self.url = reverse(
            'meetingroom:schedule:update-destroy',
            kwargs={'pk': self.schedule_item.pk},
        )

    def test_updating_period(self):
        self.data['start'] = self.now + timedelta(minutes=30)
        self.data['end'] = self.one_hour_later + timedelta(minutes=30)

        request = self.factory.put(self.url, self.data, format='json')
        response = self.view(request, pk=self.schedule_item.pk).render()

        start = self.data['start'].isoformat()
        end = self.data['end'].isoformat()
        self.data['start'] = start.replace('+00:00', 'Z')
        self.data['end'] = end.replace('+00:00', 'Z')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, self.data)

    def test_update_fail_when_there_are_period_conflict(self):
        self.data['start'] = self.now + timedelta(hours=1)
        self.data['end'] = self.one_hour_later + timedelta(hours=1)
        ScheduleItem.objects.create(
            title=self.data.get('title'),
            room=self.room,
            start=self.data.get('start'),
            end=self.data.get('end'),
        )
        request = self.factory.put(self.url, self.data, format='json')
        response = self.view(request, pk=self.schedule_item.pk).render()
        error_detail = response.data['room'][0]
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(error_detail.code, 'conflict')
        self.assertEqual(
            str(error_detail),
            'The room is already booked in this period.'
        )

    def test_updating_room(self):
        room = Room.objects.create(
            name='Edifício Baxter',
            slug='edificio-baxter',
        )
        self.data['room'] = room.pk
        request = self.factory.put(self.url, self.data, format='json')
        response = self.view(request, pk=self.schedule_item.pk).render()

        start = self.data['start'].isoformat()
        end = self.data['end'].isoformat()
        self.data['start'] = start.replace('+00:00', 'Z')
        self.data['end'] = end.replace('+00:00', 'Z')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, self.data)

    def test_update_fail_when_there_are_period_conflict_just_changing_room(self):  # noqa: E501
        room = Room.objects.create(
            name='Edifício Baxter',
            slug='edificio-baxter',
        )
        self.data['start'] = self.now + timedelta(hours=1)
        self.data['end'] = self.one_hour_later + timedelta(hours=1)
        self.data['room'] = room.pk
        ScheduleItem.objects.create(
            title=self.data.get('title'),
            room=room,
            start=self.data.get('start'),
            end=self.data.get('end'),
        )
        request = self.factory.put(self.url, self.data, format='json')
        response = self.view(request, pk=self.schedule_item.pk).render()
        error_detail = response.data['room'][0]
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(error_detail.code, 'conflict')
        self.assertEqual(
            str(error_detail),
            'The room is already booked in this period.'
        )

    def test_deleting_a_schedule_item(self):
        request = self.factory.delete(self.url)
        response = self.view(request, pk=self.schedule_item.pk).render()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(ScheduleItem.objects.exists())
