from django.urls import path

from applications.oauth.views import (
    create_tokens,
    update_tokens,
    sign_in
)


urlpatterns = [
    path('create-tokens/', create_tokens, name='create-tokens'),
    path('update-tokens/', update_tokens, name='update-tokens'),
    path('sign-in/', sign_in, name='sign-in'),
]
