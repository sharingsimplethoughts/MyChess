from django.urls import path
from .views import *
app_name='ap_leaderboard'
urlpatterns = [
    path('list',LeaderBoardListView.as_view(),name='apl_list'),
    path('detail/<int:pk>/<int:rank>',LeaderDetailView.as_view(),name='leader_detail'),
    path('export',LeaderBoardExportView.as_view(),name='leaderboard_export'),
    path('player-point-detail/<int:pk>/<int:tid>',PlayerPointDetailView.as_view(),name='player_point_detail'),
    path('player-point-detail/export',PlayerPointDetailExportView.as_view(),name='player_point_detail_export'),
]
