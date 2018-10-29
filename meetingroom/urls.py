from django.urls import include, path

from . import views


app_name = 'meetingroom'

urlpatterns = [
    path('', views.CreateRoomAPIView.as_view(), name='create'),
    path(
        '<int:pk>/',
        views.UpdateDestroyRoomAPIView.as_view(),
        name='update-destroy'
    ),
    path('schedule/', include('schedule.urls', namespace='schedule')),
]
