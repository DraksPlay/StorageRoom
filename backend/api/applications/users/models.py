from django.db import models
from decimal import Decimal

from applications.mixins import DateTimeMixin


class User(DateTimeMixin):
    email = models.EmailField(max_length=255)
    password = models.CharField(max_length=64)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal(0))

    def __str__(self):
        return self.email
