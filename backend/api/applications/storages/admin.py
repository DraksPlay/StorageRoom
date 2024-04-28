from django.contrib import admin

from applications.storages.models import (
    Category,
    Storage
)

admin.site.register(Category)
admin.site.register(Storage)
