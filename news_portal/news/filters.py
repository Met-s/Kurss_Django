from django_filters import FilterSet
from .models import Post, PostCategory


class PostFilter(FilterSet):
    class Meta:
        model = Post
        fields = {
            'post_title': ['icontains'],
            'postcategory__category_through': ['exact'],
            'post_date': ['lt']
        }
