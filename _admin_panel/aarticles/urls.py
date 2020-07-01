from django.urls import path
from .views import *

app_name='ap_articles'
urlpatterns=[
    path('article',ArticleView.as_view(),name='article'),
    path('article/dt/',DateWiseArticleView.as_view(),name='article_dt'),
    path('add_article',AddArticleView.as_view(),name='add_article'),
    path('view_article/<int:pk>',ViewArticleView.as_view(),name='view_article'),
    path('edit_article/<int:pk>',EditArticleView.as_view(),name='edit_article'),
    path('import',ImportArticleView.as_view(),name='import_article'),
]