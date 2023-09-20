from django.urls import path
from .views import (PostList, PostDetail, NewsCreate, ArticleCreate,
                    NewsUpdate, ArticleUpdate, NewsDelete)


urlpatterns = [
    path('', PostList.as_view(), name='news'),
    path('<int:pk>', PostDetail.as_view(), name='post_detail'),
    path('news/create/', NewsCreate.as_view(), name='news_create'),
    path('articles/create/', ArticleCreate.as_view(), name='article_create'),
    path('news/<int:pk>/edit/', NewsUpdate.as_view(), name='news_edit'),
    path('articles/<int:pk>/edit/', ArticleUpdate.as_view(), name='article_edit'),
    path('news/<int:pk>/delete/', NewsDelete.as_view(), name='post_delete'),
    path('articles/<int:pk>/delete/', NewsDelete.as_view(), name='post_delete'),
]