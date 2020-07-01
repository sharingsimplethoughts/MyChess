from django.urls import path
from .views import *
app_name='ap_achivement'
urlpatterns = [
    path('list',AchivementListView.as_view(),name='apac_list'),
    path('add',AddAchievementView.as_view(),name='apac_add'),
    path('import',ImportAchievementView.as_view(),name='apac_import'),
]
