from django.urls import path

from applications.storages.views import (
    create_storage,
    read_storage,
    read_storages,
    read_categories
)

urlpatterns = [
    path('create_storage/', create_storage, name='create_storage'),
    path('read_storages/', read_storages, name='read_storages'),
    path('read_storage/<int:storage_id>', read_storage, name='read_storage'),

    path('read_categories/', read_categories, name='read_categories'),
]
