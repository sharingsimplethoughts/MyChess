from django.urls import path
from .views import *

app_name = 'ap_puzzles'

urlpatterns = [
    path('categories',PuzzleCategoriesListView.as_view(),name='ap_p_categories'),
    path('categories/add',PuzzleCategoriesAddView.as_view(),name='ap_p_categories_add'),
    path('categories/view/<int:pk>',PuzzleCategoriesViewView.as_view(),name='ap_p_categories_view'),
    path('categories/edit/<int:pk>',PuzzleCategoriesEditView.as_view(),name='ap_p_categories_edit'),
    path('categories/import',PuzzleCategoriesImportView.as_view(),name='ap_p_categories_import'),
    path('list',PuzzlesListView.as_view(),name='ap_p_puzzles'),
    path('list/add',PuzzlesAddView.as_view(),name='ap_p_puzzles_add'),
    path('list/view/<int:pk>',PuzzlesViewView.as_view(),name='ap_p_puzzles_view'),
    path('list/edit/<int:pk>',PuzzlesEditView.as_view(),name='ap_p_puzzles_edit'),
    path('list/import',PuzzlesImportView.as_view(),name='ap_p_puzzles_import'),
]
