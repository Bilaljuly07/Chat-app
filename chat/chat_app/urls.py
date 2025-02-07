from django.urls import path
from .views import (
    create_organization, delete_organization, update_organization,
    add_user, delete_user, update_user, send_message, get_messages
)

urlpatterns = [
    # Organization APIs
    path('organization/create/', create_organization, name='create_organization'),
    path('organization/delete/', delete_organization, name='delete_organization'),
    path('organization/update/', update_organization, name='update_organization'),

    # User APIs
    path('user/add/', add_user, name='add_user'),
    path('user/delete/', delete_user, name='delete_user'),
    path('user/update/', update_user, name='update_user'),

    # Message APIs
    path('message/send/', send_message, name='send_message'),
    path('message/get/', get_messages, name='get_messages'),
]
