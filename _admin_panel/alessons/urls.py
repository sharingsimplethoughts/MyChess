from django.urls import path
from .views import *

app_name = 'ap_lessons'

urlpatterns = [
    path('categories',LessionCategoriesListView.as_view(),name='ap_l_categories'),
    path('categories/add',LessionCategoriesAddView.as_view(),name='ap_l_categories_add'),
    path('categories/view/<int:pk>',LessionCategoriesViewView.as_view(),name='ap_l_categories_view'),
    path('categories/edit/<int:pk>',LessionCategoriesEditView.as_view(),name='ap_l_categories_edit'),
    path('categories/import',LessionCategoriesImportView.as_view(),name='ap_l_categories_import'),
    path('list',LessionsListView.as_view(),name='ap_l_lessions'),
    path('list/add',LessionsAddView.as_view(),name='ap_l_lessions_add'),
    path('list/view/<int:pk>',LessionsViewView.as_view(),name='ap_l_lessions_view'),
    path('list/edit/<int:pk>',LessionsEditView.as_view(),name='ap_l_lessions_edit'),
    path('list/import',LessionsImportView.as_view(),name='ap_l_lessions_import'),
]
