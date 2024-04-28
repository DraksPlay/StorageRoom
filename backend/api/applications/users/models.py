from django.db import models

from applications.mixins import DateTimeMixin


class User(DateTimeMixin):
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=64)
    balance = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return self.email
