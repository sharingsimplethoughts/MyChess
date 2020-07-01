from django.urls import path
from .views import *
app_name='puzzles'
urlpatterns = [
    path('blockunblock/<int:pk>',BlockUnblockPuzzleView.as_view(),name='p_block'),
    path('delete/<int:pk>',DeletePuzzleView.as_view(),name='p_delete'),
    path('blockunblocklc/<int:pk>',BlockUnblockPuzzleCatView.as_view(),name='pc_block'),
    path('deletelc/<int:pk>',DeletePuzzleCatView.as_view(),name='pc_delete'),

    path('puzzle-cat-list',PuzzleCatListView.as_view(),name='p_cat_list'),
    path('puzzle-cat-detail/<int:pk>',PuzzleCatDetailView.as_view(),name='p_cat_detail'),
    path('puzzle-list',PuzzleListView.as_view(),name='p_list'),
    path('puzzle-detail/<int:pk>',PuzzleDetailView.as_view(),name='p_detail'),

    path('puzzle-solved',PuzzleSolvedView.as_view(),name='p_solved')
]
