from django.core.management.base import BaseCommand, CommandError
from news.models import Post, Category
from pprint import pprint


class Command(BaseCommand):
    help = 'Удаляет статьи выбранной категории'
    requires_migrations_checks = True

    def add_arguments(self, parser):
        parser.add_argument('category', type=str)

    def handle(self, *args, **options):
        answer = input(f'Вы правда хотите удалить все статьи в категории '
                       f'{options["category"]}? yes/no :')

        if answer != 'yes':
            self.stdout.write(self.style.ERROR('Отменено'))
            return
        try:
            category = Category.objects.get(category_name=options['category'])
            Post.objects.filter(post_category=category).delete()
            self.stdout.write(self.style.SUCCESS(f'Все статьи категории '
                                                 f'{category.category_name} удалены!'))
        except Post.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'Не удалось найти категорию : '
                                               f'{category.category_name}'))

