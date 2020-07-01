from django.urls import path
from .views import *

app_name = "category"

urlpatterns = [
    path('cat_list',CategoryListView.as_view(),name='list'),
    path('video_detail/<int:pk>',VideoDetailView.as_view(),name='video_detail'),
]

