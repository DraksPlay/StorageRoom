from django.db import models


class User(models.Model):
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=64)
    balance = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return self.email
