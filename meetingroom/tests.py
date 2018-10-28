from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase, APIRequestFactory

from .models import Room
from .views import CreateRoomAPIView, UpdateDestroyRoomAPIView


class CreateRoomTest(APITestCase):

    def setUp(self):
        self.view = CreateRoomAPIView.as_view()
        self.factory = APIRequestFactory()
        self.url = reverse('meetingroom:create')
        self.data = {
            'name': 'Sala da Justiça',
            'slug': 'sala-da-justica',
        }

    def test_create_room(self):
        request = self.factory.post(self.url, self.data, format='json')
        response = self.view(request).render()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, self.data)

    def test_create_room_fail_when_slug_already_exist(self):
        Room.objects.create(name=self.data['name'], slug=self.data['slug'])
        request = self.factory.post(self.url, self.data, format='json')
        response = self.view(request).render()
        error_detail = response.data['slug'][0]
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(error_detail.code, 'unique')
        self.assertEqual(
            str(error_detail),
            'room with this slug already exists.',
        )


class UpdateDestroyRoomTest(APITestCase):

    def setUp(self):
        self.view = UpdateDestroyRoomAPIView.as_view()
        self.factory = APIRequestFactory()
        self.data = {
            'name': 'Sala da Justiça',
            'slug': 'sala-da-justica',
        }
        self.url = reverse(
            'meetingroom:update-destroy',
            kwargs={'slug': self.data['slug']}
        )
        Room.objects.create(name=self.data['name'], slug=self.data['slug'])

    def test_update_name_and_slug_room(self):
        data = {
            'name': 'BatCaverna',
            'slug': 'batcaverna',
        }
        request = self.factory.put(self.url, data, format='json')
        response = self.view(request, slug=self.data.get('slug')).render()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, data)

    def test_update_fail_when_slug_already_exist(self):
        data = {
            'name': 'BatCaverna',
            'slug': 'torre-stark',
        }
        Room.objects.create(name='Torre Stark', slug=data.get('slug'))
        request = self.factory.put(self.url, data, format='json')
        response = self.view(request, slug=self.data.get('slug')).render()
        error_detail = response.data['slug'][0]
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(error_detail.code, 'unique')
        self.assertEqual(
            str(error_detail),
            'room with this slug already exists.',
        )

    def test_delete_a_room(self):
        request = self.factory.delete(self.url)
        response = self.view(request, slug=self.data.get('slug')).render()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Room.objects.exists())
