from rest_framework import status
from rest_framework.exceptions import APIException


class ScheduleConflict(APIException):
    status_code = status.HTTP_409_CONFLICT
