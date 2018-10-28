from django.urls import include, path

from . import views


app_name = 'meetingroom'

urlpatterns = [
    path('', views.CreateRoomAPIView.as_view(), name='create'),
    path('schedule/', include('schedule.urls', namespace='schedule')),
    path(
        '<slug:slug>/',
        views.UpdateDestroyRoomAPIView.as_view(),
        name='update-destroy'
    ),
]
