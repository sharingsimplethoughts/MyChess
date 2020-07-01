from django.urls import path
from .views import *
app_name='ap_tournament'
urlpatterns = [
    path('tournament_list',AllTournamentListView.as_view(),name='tournament_list'),
    path('filter_tournament_list',FilterTournamentView.as_view(),name='filter_tournament_list'),
    path('add_tournament',AddTournamentView.as_view(),name='add_tournment'),
    path('view_tournament/<int:pk>',ViewTournament.as_view(),name='view_tournament'),
    path('import_tournament',ImportTournamentView.as_view(),name='import_tournment'),
]
