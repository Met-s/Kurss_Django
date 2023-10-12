from pprint import pprint

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.template.loader import render_to_string

from .models import PostCategory


def send_notification(preview, pk, post_title, subscribers):
    html_content = render_to_string(
        'post_email.html',
        {
            'text': preview,
            'link': f'{settings.SITE_URL}/news/{pk}'
        }
    )
    msg = EmailMultiAlternatives(
        subject=post_title,
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers,
    )
    msg.attach_alternative(html_content, 'text/html')
    msg.send()


@receiver(m2m_changed, sender=PostCategory)
def post_created(sender, instance, **kwargs):
    if kwargs['action'] == 'post_add':
        categories = instance.post_category.all()
        subscribers: list[str] = []
        pprint(f'categories : {categories}')
        for category in categories:
            subscribers += category.category_sub.all()
        subscribers = [s.user.email for s in subscribers]
        send_notification(instance.preview(), instance.pk, instance.post_title,
                          subscribers)
