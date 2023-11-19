from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.core.cache import cache


class Author(models.Model):
    """
    Модель Author имя и рейтинг авторов:
    author_user (имя автора)
    author_rating (рейтинг автора)
    """
    author_user = models.OneToOneField(User, on_delete=models.CASCADE)
    author_rating = models.SmallIntegerField(default=0)

    def update_rating(self):
        """
        Считает рейтинг автора (суммирует рейтинги постов и комментов)
        """
        post_rat = self.post_set.aggregate(postrating=Sum('post_rating'))
        prat = 0
        prat += post_rat.get('postrating')

        comment_rat = self.author_user.comment_set.aggregate(
            commentrating=Sum('comment_rating'))
        crat = 0
        crat += comment_rat.get('commentrating')

        self.author_rating = prat * 3 + crat
        self.save()

    def __str__(self):
        return f'{self.author_user.username} : {self.author_rating}'


class Category(models.Model):
    """
    Модель Category список всех категорий:
    category_name(имя категории  max_length=64)
    """
    category_name = models.CharField(max_length=64, unique=True)
    subscribers = models.ManyToManyField(User, related_name='categories',
                                         default='')

    def __str__(self):
        return f'{self.category_name}'


class Post(models.Model):
    """
    Модель Post статьи:
    post_author(имя автора написавшего статью),
    category_type(тип статьи NW,AR),
    post_date(дата написания статьи),
    post_category(категория статьи связь ManyToMany с моделью Category),
    post_title(заголовок статьи, 128 символов),
    post_rating(рейтинг статьи),
    preview(метод краткое содержание статьи max_length=128)
    """
    news = 'NW'
    article = 'AR'

    CATEGORY_CHOICES = [
        (news, 'Новость'),
        (article, 'Статья')
    ]
    post_author = models.ForeignKey(Author, on_delete=models.CASCADE)
    category_type = models.CharField(max_length=2, choices=CATEGORY_CHOICES,
                                     default=article)
    post_date = models.DateTimeField(auto_now_add=True)
    post_category = models.ManyToManyField(Category, through='PostCategory')
    post_title = models.CharField(max_length=128)
    post_text = models.TextField()
    post_rating = models.SmallIntegerField(default=0)

    def __str__(self):
        return (f'{self.post_date} : {self.category_type} : '
                f'{self.post_title} : {self.post_text} : {self.post_category}')

    def like(self):
        self.post_rating += 1
        self.save()

    def dislike(self):
        self.post_rating -= 1
        self.save()

    def preview(self):
        return self.post_text[0:125] + '...'

    def get_absolute_url(self):
        return f'/news/{self.pk}'
        # return reverse('post_detail', args=[str(self.id)])

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        cache.delete(f'post-{self.pk}')


class PostCategory(models.Model):
    """
    Промежуточная Модель категорий стаей:
    post_through(связь с моделью Post),
    category_through(связь с моделью Category)
    """
    post_through = models.ForeignKey(Post, on_delete=models.CASCADE)
    category_through = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.post_through}'


class Comment(models.Model):
    """
    Модель Comment комментарии к статье:
    comment_post(текст статьи на которую написали комментарий),
    comment_user(имя пользователя написавшего комментарий),
    comment_text(текст комментария),
    comment_date(дата когда был написан комментарий),
    comment_rating(рейтинг комментария).
    """
    comment_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment_user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_text = models.TextField()
    comment_date = models.DateTimeField(auto_now_add=True)
    comment_rating = models.SmallIntegerField(default=0)

    def __str__(self):
        return (f'{self.comment_post} : {self.comment_user} : '
                f'{self.comment_text} : {self.comment_date} : '
                f'{self.comment_rating}')

    def like(self):
        self.comment_rating += 1
        self.save()

    def dislike(self):
        self.comment_rating -= 1
        self.save()


class Subscriber(models.Model):
    """
    Модель Subscriber промежуточная модель Подписчики:
    user(связь с моделью User имя пользователя(подписчика))
    category(связь с моделью Category, категория на которую подписан
    пользователь)
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='user_sub')
    category = models.ForeignKey(Category,
                                 on_delete=models.CASCADE,
                                 related_name='category_sub')

    def __str__(self):
        return f'{self.user} : {self.category}'
