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
        self.data = {'name': 'Sala da Justiça'}

    def test_create_room(self):
        request = self.factory.post(self.url, self.data, format='json')
        response = self.view(request).render()
        self.data['pk'] = Room.objects.first().pk
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, self.data)


class UpdateDestroyRoomTest(APITestCase):

    def setUp(self):
        self.view = UpdateDestroyRoomAPIView.as_view()
        self.factory = APIRequestFactory()
        self.data = {'name': 'Sala da Justiça'}
        self.room = Room.objects.create(name=self.data['name'])
        self.url = reverse(
            'meetingroom:update-destroy',
            kwargs={'pk': self.room.pk}
        )

    def test_update_name_room(self):
        data = {'name': 'BatCaverna'}
        request = self.factory.put(self.url, data, format='json')
        response = self.view(request, pk=self.room.pk).render()
        data['pk'] = self.room.pk
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, data)

    def test_delete_a_room(self):
        request = self.factory.delete(self.url)
        response = self.view(request, pk=self.room.pk).render()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Room.objects.exists())
