from django.core.management.base import BaseCommand, CommandError
from news.models import Post, Category


class Command(BaseCommand):
    help = 'Убирает все новости категории'

    def add_arguments(self, parser):
        parser.add_argument('category', type=str)

    def handle(self, *args, **options):
        answer = input(f'Вы правда хотите удалить все статьи в категории {options["category"]}? yes/no')
         if answer == 'no':
             self.stdout.write(self.style.ERROR('Отменено'))
             return
         try:
             category = Category.objects.get(name=options['category'])
             Post.objects.filter(category=category).delete()
             self.stdout.write(self.style.SUCCESS(f'Успешно {category.name}'))
         except: Category.DoesNotExist
             self.stdout.write(self.style.ERROR(f'Такой категории нет {options["category"]}'))

