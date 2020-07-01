from django.urls import path
from .views import *
app_name="ap_notification"
urlpatterns = [
    path('send_notification',SendNotification.as_view(),name='ap_nm_send_notification'),
    path('add_recipient',AddRecipientView.as_view(),name='ap_nm_add_recipient'),
    path('create_group',CreateGroupView.as_view(),name='ap_nm_create_group'),
]
