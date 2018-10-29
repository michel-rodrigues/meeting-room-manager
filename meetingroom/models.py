from django.db import models

from commons.base_models import BaseModel


class Room(BaseModel):
    name = models.CharField(max_length=120)
