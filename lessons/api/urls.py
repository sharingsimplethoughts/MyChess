from django.urls import path
from .views import *
app_name='lessons'
urlpatterns = [
    path('blockunblock/<int:pk>',BlockUnblockLessonView.as_view(),name='l_block'),
    path('delete/<int:pk>',DeleteLessonView.as_view(),name='l_delete'),
    path('blockunblocklc/<int:pk>',BlockUnblockLessonCatView.as_view(),name='lc_block'),
    path('deletelc/<int:pk>',DeleteLessonCatView.as_view(),name='lc_delete'),

    path('lesson-cat-list',LessonCatListView.as_view(),name='l_cat_list'),
    path('lesson-cat-detail/<int:pk>',LessonCatDetailView.as_view(),name='l_cat_detail'),
    path('lesson-list',LessonListView.as_view(),name='l_list'),
    path('lesson-detail/<int:pk>',LessonDetailView.as_view(),name='l_detail'),
    path('lesson-detail-temp/<int:pk>',LessonDetailTempView.as_view(),name='l_detail_temp'),

    path('lesson-solved',LessonSolvedView.as_view(),name='l_solved')
    
]
