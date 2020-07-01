from django.urls import path
from .views import *

app_name='articles'

urlpatterns=[
    path('list',ArticlesListView.as_view(),name='list'),
    path('detail/<int:pk>',ArticleDetailView.as_view(),name='art_detail'),
    path('create',CreateArticleView.as_view(),name='create'),
    path('delete/<int:pk>',DeleteArticleView.as_view(),name='delete'),

    path('video_category_list',VideoCategoryListView.as_view(),name='v_cat_list'),
    path('video_detail/<int:pk>',VideoDetailView.as_view(),name='v_detail'),
    path('add_video_comment',AddVideoCommentView.as_view(),name="add_video_comment"),
    path('delete_video_cat/<int:pk>',VideoCategoryDeleteView.as_view(),name='v_delete_cat'),
    path('block_unblock_video_cat/<int:pk>',BlockUnblockVideoCategoryView.as_view(),name='v_block_unblock_cat'),

    path('delete_video/<int:pk>',VideoDeleteView.as_view(),name='v_delete'),
    path('block_unblock_video/<int:pk>',BlockUnblockVideoView.as_view(),name='v_block_unblock'),

    # path('add_temp_video',AddTempVideoView.as_view(),name='v_add_temp'),
    # path('remove_temp_video/<int:pk>',RemoveTempVideoView.as_view(),name='v_remove_temp'),    
]