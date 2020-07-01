from django.urls import *

from .views import *
app_name='ap_usermgmt'
urlpatterns = [
    path('list',UserManagementListView.as_view(),name='ap_um_list'),
    path('export',UserExportView.as_view(),name='ap_um_export'),
    path('detail/<int:pk>',UserDetailView.as_view(),name='ap_um_detail'),
]