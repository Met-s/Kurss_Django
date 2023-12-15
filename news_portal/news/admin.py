from django.contrib import admin
from .models import Author, Post, Category, Comment, Subscriber
from modeltranslation.admin import TranslationAdmin


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


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('author_user', 'author_rating')


class SubscriberAdmin(admin.ModelAdmin):
    list_display = ('user', 'category')
    list_filter = ('user', 'category__category_name')


class AuthorAdmin(TranslationAdmin):
    model = Author


class CategoryAdmin(TranslationAdmin):
    model = Category


class PostAdmin(TranslationAdmin):
    model = Post


class CommentAdmin(TranslationAdmin):
    model = Comment


admin.site.register(Author, AuthorAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Subscriber, SubscriberAdmin)
