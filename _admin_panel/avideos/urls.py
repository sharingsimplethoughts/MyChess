from django.urls import path
from .views import *

app_name="ap_videos"

urlpatterns = [
    path('videos',VideosView.as_view(),name='ap_vid_videos'),
    path('video_categories',VideosCategoriesView.as_view(),name='ap_vid_video_categories'),
    path('add_video',AddVideoView.as_view(),name='ap_vid_add_video'),
    path('edit_video/<int:pk>',EditVideoView.as_view(),name='ap_vid_edit_video'),
    path('edit_video_cat/<int:pk>',EditVideoCatView.as_view(),name='ap_vid_edit_video_cat'),
    path('add_video_cat',AddVideoCatView.as_view(),name='ap_vid_add_video_cat'),
    path('view_video/<int:pk>',ViewVideoView.as_view(),name='ap_vid_view_video'),
    path('view_video_cat/<int:pk>',ViewVideoCatView.as_view(),name='ap_vid_view_video_cat'),
    path('import_video',ImportVideoView.as_view(),name='ap_vid_import_video'),
    path('import_video_cat',ImportVideoCategoryView.as_view(),name='ap_vid_import_video_cat'),
]