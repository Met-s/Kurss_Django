from django.contrib import admin
from .models import Author, Post, Category, Comment, Subscriber


class PostAdmin(admin.ModelAdmin):
    list_display = ('post_date', 'category', 'post_author', 'category_type',
                    'post_title', 'post_rating')
    list_filter = ('post_date', 'post_category__category_name', 'post_author',
                   'category_type',
                   'post_rating')

    def category(self, post):
        """
        Метод выводит категорию поста, при связи ManyToMany
        """
        return ', '.join([_.category_name for _ in post.post_category.all()])


class CommentAdmin(admin.ModelAdmin):
    list_display = ('comment_post', 'comment_user', 'comment_text',
                    'comment_date', 'comment_rating')
    list_filter = ('comment_user', 'comment_date', 'comment_rating')


admin.site.register(Author)
admin.site.register(Post, PostAdmin)
admin.site.register(Category)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Subscriber)
