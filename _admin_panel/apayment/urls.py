from django.urls import path
from .views import *
app_name='ap_payment'
urlpatterns = [
    path('list',PaymentListView.as_view(),name='appay_list'),
    path('export',PaymentListExportView.as_view(),name='appay_export'),
]
