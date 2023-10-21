from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from news.models import Post, Subscriber, PostCategory
from news_portal import settings
from datetime import datetime, timedelta


@shared_task
def send_email_task(pk):
    posts = Post.objects.get(pk=pk)
    categories = posts.post_category.all()
    subscribers: list[str] = []
    for category in categories:
        subscribers += category.category_sub.all()
    subscribers = [s.user.email for s in subscribers]

    html_content = render_to_string(
        'post_email.html',
        {
            'text': posts.preview,
            'link': f'{settings.SITE_URL}/news/{pk}'
        }
    )
    msg = EmailMultiAlternatives(
        subject=posts.post_title,
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers,
    )
    msg.attach_alternative(html_content, 'text/html')
    msg.send()


@shared_task
def post_weekly_notification():
    today = datetime.now()
    last_week = today - timedelta(days=7)
    posts = Post.objects.filter(post_date__gte=last_week)
    categories = set(
        posts.values_list('post_category__category_name', flat=True))
    # --------------------------------------------------
    subscribers = set(Subscriber.objects.filter(
        category__category_name__in=categories))

    subscribers_cat = set(s.category for s in subscribers)
    pos = set(posts.filter(post_category__category_name__in=subscribers_cat))
    subscriber = set(s.user.email for s in subscribers)
    # --------------------------------------------------
    html_content = render_to_string(
        'weekly_post.html',
        {
            'link': settings.SITE_URL,
            'posts': pos,
        }
    )
    msg = EmailMultiAlternatives(
        subject='Статьи за неделю',
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscriber,
    )

    msg.attach_alternative(html_content, 'text/html')
    msg.send()
