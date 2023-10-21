from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from news.models import Post, Subscriber, PostCategory
from news_portal import settings


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
