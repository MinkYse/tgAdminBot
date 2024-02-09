import json

from django.core.management.base import BaseCommand

from bot.models import Category, Region


class Command(BaseCommand):
    ''' Загрузка данных из JSON-файла '''

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING('Загружаем категории!'))
        categories_file_path = 'data/categories.json'
        try:
            with open(categories_file_path,
                      encoding='utf-8') as data_file_categories:
                categories_data = json.load(data_file_categories)
                for category in categories_data:
                    Category.objects.get_or_create(**category)
        except FileNotFoundError:
            self.stdout.write(
                self.style.ERROR('Файл с категориями не найден!'))
        except json.JSONDecodeError:
            self.stdout.write(
                self.style.ERROR(
                    'Ошибка при чтении JSON файла с категориями!'))

        self.stdout.write(self.style.WARNING('Загружаем регионы!'))
        regions_file_path = 'data/regions.json'
        try:
            with open(regions_file_path,
                      encoding='utf-8') as data_file_regions:
                regions_data = json.load(data_file_regions)
                for region in regions_data:
                    Region.objects.get_or_create(**region)
        except FileNotFoundError:
            self.stdout.write(
                self.style.ERROR('Файл с регионами не найден!'))
        except json.JSONDecodeError:
            self.stdout.write(
                self.style.ERROR(
                    'Ошибка при чтении JSON файла с регионами!'))

        self.stdout.write(self.style.SUCCESS('Отлично загрузили!'))