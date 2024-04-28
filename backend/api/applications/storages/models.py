from django.db import models

from applications.mixins import DateTimeMixin
from applications.users.models import User


class Category(DateTimeMixin):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return self.name


class Storage(DateTimeMixin):
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    start_at = models.DateTimeField()
    finish_at = models.DateTimeField()

    def __str__(self):
        return f"Storage(Category: {self.category.name}, User: {self.user.name})"

