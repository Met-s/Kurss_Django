from django.urls import path
from .views import (PostList, PostDetail, NewsCreate, ArticleCreate,
                    NewsUpdate, ArticleUpdate, NewsDelete, NewsSearch,
                     )
from django.views.decorators.cache import cache_page


urlpatterns = [
    path('', cache_page(60)(PostList.as_view()), name='news'),  # 1m
    path('<int:pk>', cache_page(60*5)(PostDetail.as_view()),
         name='post_detail'),  # 5m
    path('create/', NewsCreate.as_view(), name='news_create'),
    path('articles/create/', ArticleCreate.as_view(), name='article_create'),
    path('<int:pk>/edit/', NewsUpdate.as_view(), name='news_edit'),
    path('articles/<int:pk>/edit/', ArticleUpdate.as_view(),
         name='article_edit'),
    path('<int:pk>/delete/', NewsDelete.as_view(), name='post_delete'),
    path('articles/<int:pk>/delete/', NewsDelete.as_view(), name='post_delete'),
    path('search/', NewsSearch.as_view(), name='news_search'),

]
