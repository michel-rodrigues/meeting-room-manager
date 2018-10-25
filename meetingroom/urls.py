from django.urls import path

from . import views


app_name = 'meetingroom'

urlpatterns = [
    path(
        'create/',
        views.CreateRoomAPIView.as_view(),
        name='create'
    ),
]
