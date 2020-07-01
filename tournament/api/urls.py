from django.urls import path
from .views import *
app_name="tournament"


urlpatterns = [
    path('available_list',AvailableTournamentListView.as_view(),name='t_avlist'),
    path('joined_list',JoinedTournamentListView.as_view(),name='t_jlist'),
    path('join',JoinTournamentView.as_view(),name='t_join'),
    path('standings/<int:pk>',TournamentStandingsView.as_view(),name='t_standings'),
    path('user_status',UserTournamentStatusView.as_view(),name='t_user_status'),
    path('delete/<int:pk>',DeleteTournamentView.as_view(),name='t_delete'),
    path('rate_tournament',RateTournamentView.as_view(),name='t_rate'),

    path('special_api',SpecialApiView.as_view(),name='special_api'),
]
