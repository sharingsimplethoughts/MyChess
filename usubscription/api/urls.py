from django.urls import path
from .views import *

app_name = "usubscription"

urlpatterns = [
    path('get_plan_list',GetPlanListView.as_view(),name='get_plan_list'),

    path('block_unblock/<int:pk>',BlockUnclockSubscriptionView.as_view(),name='usub_block_unblock'),
    path('delete/<int:pk>',DeleteSubscriptionView.as_view(),name='usub_delete'),
]