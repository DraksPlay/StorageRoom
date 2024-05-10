from django.urls import path

from applications.oauth.views import (
    create_tokens,
    update_tokens,
)


urlpatterns = [
    path('create_tokens/', create_tokens, name='create_tokens'),
    path('update_tokens/', update_tokens, name='update_tokens'),
]
