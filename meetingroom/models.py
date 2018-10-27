from django.db import models

from commons.base_models import BaseModel


class Room(BaseModel):
    name = models.CharField(max_length=120)
    slug = models.SlugField(max_length=150, unique=True)
