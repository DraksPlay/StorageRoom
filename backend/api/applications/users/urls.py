from django.urls import path

from applications.users.views import (
    create_user,
    read_user,
    read_users,
    update_user,
    delete_user
)

urlpatterns = [
    path('create_user/', create_user, name='create_user'),
    path('read_users/', read_users, name='read_users'),
    path('read_user/<int:user_id>', read_user, name='read_user'),
    path('update_user/<int:user_id>', update_user, name='update_user'),
    path('delete_user/<int:user_id>', delete_user, name='delete_user'),
]
