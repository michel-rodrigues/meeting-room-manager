from datetime import timedelta

from django.urls import reverse
from django.utils import timezone

from rest_framework import status
from rest_framework.test import APITestCase, APIRequestFactory

from meetingroom.models import Room
from ..models import ScheduleItem
from ..views import ListCreateScheduleItemAPIView


class ListCreateScheduleItemTest(APITestCase):

    def setUp(self):
        self.now = timezone.now()
        self.one_hour_later = self.now + timedelta(hours=1)
        self.view = ListCreateScheduleItemAPIView.as_view()
        self.factory = APIRequestFactory()
        self.url = reverse('meetingroom:schedule:list-create')
        self.data = {
            'title': 'Planning Novos Negócios',
            'room': 'torre-stark',
            'start': self.now,
            'end': self.one_hour_later,
        }
        self.room = Room.objects.create(
            name='Torre Stark',
            slug=self.data.get('room'),
        )

    def test_create_item_schedule(self):
        request = self.factory.post(self.url, self.data, format='json')
        response = self.view(request).render()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_fail_create_item_schedule_when_room_slug_is_missing(self):
        self.data.pop('room')
        request = self.factory.post(self.url, self.data, format='json')
        response = self.view(request).render()
        error_detail = response.data['room'][0]
        self.assertEqual(error_detail.code, 'required')
        self.assertEqual(str(error_detail), 'This field is required.')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_fail_create_item_schedule_when_room_does_not_exist(self):
        self.data['room'] = 'batcaverna'
        request = self.factory.post(self.url, self.data, format='json')
        response = self.view(request).render()
        error_detail = response.data['room'][0]
        self.assertEqual(error_detail.code, 'required')
        self.assertEqual(str(error_detail), "Room doesn't exist")
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
