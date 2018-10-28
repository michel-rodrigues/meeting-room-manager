from django.urls import path

from . import views


app_name = 'schedule'

urlpatterns = [
    path(
        '',
        views.ListCreateScheduleItemAPIView.as_view(),
        name='list-create'
    ),
    path(
        '<int:pk>/',
        views.UpdateDestroyScheduleItemAPIView.as_view(),
        name='update-destroy'
    ),
]
