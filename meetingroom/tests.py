from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase, APIRequestFactory

from .models import Room
from .views import CreateRoomAPIView


class RoomTest(APITestCase):

    def setUp(self):
        self.factory = APIRequestFactory()
        self.url_create = reverse('meetingroom:create')
        self.data = {
            'name': 'Sala Teste',
            'slug': 'sala-teste',
        }

    def test_create_room(self):
        request = self.factory.post(self.url_create, self.data, format='json')
        view = CreateRoomAPIView.as_view()
        response = view(request)
        response.render()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_room_fail_when_slug_already_exist(self):
        Room.objects.create(name=self.data['name'], slug=self.data['slug'])
        request = self.factory.post(self.url_create, self.data, format='json')
        view = CreateRoomAPIView.as_view()
        response = view(request)
        response.render()
        error_detail = response.data['slug'][0]
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(error_detail.code, 'unique')
        self.assertEqual(
            error_detail.title(),
            'Room With This Slug Already Exists.',
        )
