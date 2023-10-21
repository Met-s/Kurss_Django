import datetime
import logging

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.core.mail import mail_managers
from django.core.management.base import BaseCommand
from django.template.loader import render_to_string
from django_apscheduler import util
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from news.models import Post, Category, Subscriber
from news_portal import settings

logger = logging.getLogger(__name__)


def my_job():
    today = datetime.datetime.now()
    last_week = today - datetime.timedelta(days=7)
    posts = Post.objects.filter(post_date__gte=last_week)
    categories = set(
        posts.values_list('post_category__category_name', flat=True))
    # --------------------------------------------------
    subscribers: list[str] = []
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


# @util.close_old_connections
def delete_old_job_executions(max_age=604_800):
    """
    Это задание удаляет записи выполнения заданий APScheduler старше
    максимального возраста 'max_age' из БД.
    Это помогает предотвратить заполнение БД старыми историческими данными,
    записи которые больше не нужны.
    : param max_age: максимальная продолжительность хранения исторических
    записей выполнения заданий. По умолчанию 7 дней.
    """
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs APScheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            my_job,
            trigger=CronTrigger(day_of_week="fri", hour="18", minute="00"),
            # day_of_week="fri", hour="18", minute="00"  пятница 18:00  wed
            id="my_job",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added weekly job: 'delete_old_job_executions'.")

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")
