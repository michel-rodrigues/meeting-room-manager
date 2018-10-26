from django.urls import path

from . import views


app_name = 'meetingroom'

urlpatterns = [
    path('manager/', views.CreateRoomAPIView.as_view(), name='create'),
    path(
        'manager/<slug:slug>/',
        views.UpdateDestroyRoomAPIView.as_view(),
        name='retrieve-update-destroy'
    ),
]
