from django.urls import path

from applications.oauth.views import (
    create_tokens,
    update_tokens,
    sign_in,
    check_auth
)


urlpatterns = [
    path('create-tokens/', create_tokens, name='create-tokens'),
    path('update-tokens/', update_tokens, name='update-tokens'),
    path('sign-in/', sign_in, name='sign-in'),
    path('check-auth/', check_auth, name='check-auth'),
]
