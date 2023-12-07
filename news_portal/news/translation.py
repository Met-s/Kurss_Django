from .models import Author, Category, Post, Comment, User
from modeltranslation.translator import register, TranslationOptions


@register(Author)
class AuthorTranslationOptions(TranslationOptions):
    fields = ('author_user',)


@register(User)
class UserTranslationOptions(TranslationOptions):
    fields = ('Username',)


@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('category_name',)


@register(Post)
class PostTranslationOptions(TranslationOptions):
    fields = ('post_author', 'post_title', 'post_text')


@register(Comment)
class CommentTranslationOptions(TranslationOptions):
    fields = ('comment_post', 'comment_user', 'comment_text')
