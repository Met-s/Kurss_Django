from django.contrib import admin
from .models import Author, Post, Category, PostCategory, Comment, Subscriber


class PostAdmin(admin.ModelAdmin):

    list_display = ('post_date', 'category', 'post_author', 'category_type',
                    'post_title', 'post_rating')

    def category(self, post):
        """
        Метод выводит категорию поста, при связи ManyToMany
        """
        return ', '.join([_.category_name for _ in post.post_category.all()])


admin.site.register(Author)
admin.site.register(Post, PostAdmin)
admin.site.register(Category)
admin.site.register(PostCategory)
admin.site.register(Comment)
admin.site.register(Subscriber)
