from django.urls import path
from .views import *
app_name='achievement'

urlpatterns = [
    path('list',AchievementListView.as_view(),name="ach_list"),
    path('detail/<int:pk>',AchievementDetailView.as_view(),name="ach_detail"),
    path('blockunblock/<int:pk>',BlockUnblockAchievementView.as_view(),name="ach_block"),
    path('delete/<int:pk>',DeleteAchievementView.as_view(),name="ach_delete"),

    path('ap_detail/<int:pk>',APAchievementDetailView.as_view(),name="ap_ach_detail"),
    path('ap_edit/<int:pk>',APEditAchievementView.as_view(),name="ap_ach_edit"),

    path('achievement_completed',AchievementCompletedView.as_view(),name='ach_completed')
]
