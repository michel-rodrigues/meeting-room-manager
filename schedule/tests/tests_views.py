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
    RetrieveUpdateDestroyScheduleItemAPIView,
)


class CreateScheduleItemTest(APITestCase):

    def setUp(self):
        self.now = timezone.now()
        self.one_hour_later = self.now + timedelta(hours=1)
        self.view = ListCreateScheduleItemAPIView.as_view()
        self.factory = APIRequestFactory()
        self.url = reverse('meetingroom:schedule:list-create')
        self.room = Room.objects.create(name='Torre Stark')
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
        self.data['pk'] = ScheduleItem.objects.first().pk
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, self.data)

    def test_fail_create_item_schedule_when_room_pk_is_missing(self):
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
        error_detail = response.data['detail']
        error_message = 'The room is already booked in this period.'
        self.assertEqual(error_detail.code, 'period_conflict')
        self.assertEqual(str(error_detail), error_message)
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)

    def test_fail_when_date_on_start_field_is_after_date_on_end_field(self):
        self.data['start'] = self.now + timedelta(minutes=1)
        self.data['end'] = self.now
        request = self.factory.post(self.url, self.data, format='json')
        response = self.view(request).render()
        error_detail = response.data['detail']
        error_message = 'Start date must begin before end date.'
        self.assertEqual(error_detail.code, 'inverted_date_values')
        self.assertEqual(str(error_detail), error_message)
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)


class ListCreateScheduleItemTest(APITestCase):

    def setUp(self):
        self.now = timezone.now()
        self.one_hour_later = self.now + timedelta(hours=1)
        self.view = ListCreateScheduleItemAPIView.as_view()
        self.factory = APIRequestFactory()
        self.url = reverse('meetingroom:schedule:list-create')
        self.room_1 = Room.objects.create(name='Torre Stark')
        self.serialized_room_1 = OrderedDict(
            pk=self.room_1.pk,
            name=self.room_1.name,
        )
        self.schedule_item_1 = ScheduleItem.objects.create(
            title='Planning Novos Negócios',
            room=self.room_1,
            start=self.now,
            end=self.one_hour_later,
        )
        self.serialized_schedule_item_1 = OrderedDict(
            pk=self.schedule_item_1.pk,
            title=self.schedule_item_1.title,
            room=self.serialized_room_1,
            start=(
                self.schedule_item_1.start.isoformat().replace('+00:00', 'Z')
            ),
            end=self.schedule_item_1.end.isoformat().replace('+00:00', 'Z'),
        )
        self.room_2 = Room.objects.create(name='Sala do perigo')
        self.serialized_room_2 = OrderedDict(
            pk=self.room_2.pk,
            name=self.room_2.name,
        )
        self.schedule_item_2 = ScheduleItem.objects.create(
            title='Grooming Logística',
            room=self.room_2,
            start=self.now + timedelta(hours=1),
            end=self.one_hour_later + timedelta(hours=1),
        )
        self.serialized_schedule_item_2 = OrderedDict(
            pk=self.schedule_item_2.pk,
            title=self.schedule_item_2.title,
            room=self.serialized_room_2,
            start=(
                self.schedule_item_2.start.isoformat().replace('+00:00', 'Z')
            ),
            end=self.schedule_item_2.end.isoformat().replace('+00:00', 'Z'),
        )

    def test_listing_all_items(self):
        expected_data = [
            self.serialized_schedule_item_2,
            self.serialized_schedule_item_1,
        ]
        request = self.factory.get(self.url)
        response = self.view(request).render()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)

    def test_search_items_by_room_name(self):
        room_3 = Room.objects.create(name='Casa Stark de Winterfell')
        serialized_room_3 = OrderedDict(
            pk=room_3.pk,
            name=room_3.name,
        )
        schedule_item_3 = ScheduleItem.objects.create(
            title='Planning B2B',
            room=room_3,
            start=self.now,
            end=self.one_hour_later,
        )
        serialized_schedule_item_3 = OrderedDict(
            pk=schedule_item_3.pk,
            title=schedule_item_3.title,
            room=serialized_room_3,
            start=schedule_item_3.start.isoformat().replace('+00:00', 'Z'),
            end=schedule_item_3.end.isoformat().replace('+00:00', 'Z'),
        )
        expected_data = [
            self.serialized_schedule_item_1,
            serialized_schedule_item_3,
        ]
        url_query = '{}?room={}'.format(self.url, 'stark')
        request = self.factory.get(url_query)
        response = self.view(request).render()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)

    def test_search_items_by_date(self):
        self.now = timezone.now().replace(day=27, month=10, year=2018)
        self.one_hour_later = self.now + timedelta(hours=1)

        self.schedule_item_2.start = self.now
        self.schedule_item_2.end = self.one_hour_later
        self.schedule_item_2.save()

        self.serialized_schedule_item_2['start'] = (
            self.schedule_item_2.start.isoformat().replace('+00:00', 'Z')
        )
        self.serialized_schedule_item_2['end'] = (
            self.schedule_item_2.end.isoformat().replace('+00:00', 'Z')
        )

        room_3 = Room.objects.create(name='Casa Stark de Winterfell')
        serialized_room_3 = OrderedDict(
            pk=room_3.pk,
            name=room_3.name,
        )
        schedule_item_3 = ScheduleItem.objects.create(
            title='Planning B2B',
            room=room_3,
            start=self.now,
            end=self.one_hour_later,
        )
        serialized_schedule_item_3 = OrderedDict(
            pk=schedule_item_3.pk,
            title=schedule_item_3.title,
            room=serialized_room_3,
            start=schedule_item_3.start.isoformat().replace('+00:00', 'Z'),
            end=schedule_item_3.end.isoformat().replace('+00:00', 'Z'),
        )

        expected_data = [
            self.serialized_schedule_item_2,
            serialized_schedule_item_3,
        ]

        url_query = '{}?start={}'.format(self.url, '2018-10-27')
        request = self.factory.get(url_query)
        response = self.view(request).render()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)

    def test_search_items_by_room_name_and_date(self):
        now_iso_format = self.now.date().isoformat()
        room_3 = Room.objects.create(name='Casa Stark de Winterfell')
        serialized_room_3 = OrderedDict(
            pk=room_3.pk,
            name=room_3.name,
        )
        schedule_item_3 = ScheduleItem.objects.create(
            title='Planning B2B',
            room=room_3,
            start=self.now,
            end=self.one_hour_later,
        )
        serialized_schedule_item_3 = OrderedDict(
            pk=schedule_item_3.pk,
            title=schedule_item_3.title,
            room=serialized_room_3,
            start=schedule_item_3.start.isoformat().replace('+00:00', 'Z'),
            end=schedule_item_3.end.isoformat().replace('+00:00', 'Z'),
        )

        now = timezone.now().replace(day=27, month=10, year=2018)
        one_hour_later = now + timedelta(hours=1)
        room_4 = Room.objects.create(name="Indústrias Stark")
        ScheduleItem.objects.create(
            title='Planning Marketplace',
            room=room_4,
            start=now,
            end=one_hour_later,
        )

        expected_data = [
            self.serialized_schedule_item_1,
            serialized_schedule_item_3,
        ]

        url_query = '{}?room=stark&start={}'.format(self.url, now_iso_format)
        request = self.factory.get(url_query)
        response = self.view(request).render()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)

    def test_when_not_find_items(self):
        url_query = '{}?room=Jedi&start=2018-05-04'.format(self.url)
        request = self.factory.get(url_query)
        response = self.view(request).render()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])

    def test_when_query_params_does_not_exist(self):
        expected_data = [
            self.serialized_schedule_item_2,
            self.serialized_schedule_item_1,
        ]
        url_query = '{}?bedroom=start&restart=2018-05-04'.format(self.url)
        request = self.factory.get(url_query)
        response = self.view(request).render()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)


class UpdateDestroyRoomTest(APITestCase):

    def setUp(self):
        self.now = timezone.now()
        self.one_hour_later = self.now + timedelta(hours=1)
        self.view = RetrieveUpdateDestroyScheduleItemAPIView.as_view()
        self.factory = APIRequestFactory()
        self.room = Room.objects.create(name='Torre Stark')
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
        self.data['pk'] = self.schedule_item.pk

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
        error_detail = response.data['detail']
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
        self.assertEqual(error_detail.code, 'period_conflict')
        self.assertEqual(
            str(error_detail),
            'The room is already booked in this period.'
        )

    def test_updating_room(self):
        room = Room.objects.create(name='Edifício Baxter')
        self.data['room'] = room.pk
        request = self.factory.put(self.url, self.data, format='json')
        response = self.view(request, pk=self.schedule_item.pk).render()

        start = self.data['start'].isoformat()
        end = self.data['end'].isoformat()
        self.data['start'] = start.replace('+00:00', 'Z')
        self.data['end'] = end.replace('+00:00', 'Z')
        self.data['pk'] = self.schedule_item.pk

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, self.data)

    def test_update_fail_when_there_are_period_conflict_just_changing_room(self):  # noqa: E501
        room = Room.objects.create(name='Edifício Baxter')
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
        error_detail = response.data['detail']
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
        self.assertEqual(error_detail.code, 'period_conflict')
        self.assertEqual(
            str(error_detail),
            'The room is already booked in this period.'
        )

    def test_deleting_a_schedule_item(self):
        request = self.factory.delete(self.url)
        response = self.view(request, pk=self.schedule_item.pk).render()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(ScheduleItem.objects.exists())
