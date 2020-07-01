from django.urls import path
from .views import *
app_name='ap_subscription'

urlpatterns = [
    path('list',SubscriptionListView.as_view(),name='aps_list'),
    path('add',AddSubscriptionView.as_view(),name='aps_add'),
    path('edit/<int:pk>',EditSubscriptionView.as_view(),name='aps_edit'),
    path('view/<int:pk>',ViewSubscriptionView.as_view(),name='aps_view'),
    path('import',ImportSubscriptionView.as_view(),name='aps_import'),
]
