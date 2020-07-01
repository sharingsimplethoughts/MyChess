from django.urls import path
from .views import *
# admin_panel/gametime/
app_name = 'ap_gametime'

urlpatterns = [
    path('list',ListGameTimeListView.as_view(),name='apg_list'),
    path('add',AddGameTimeView.as_view(),name='apg_add'),
    path('edit',EditGameTimeView.as_view(),name='apg_edit'),
]
