import csv
import os

from django.core.management.base import BaseCommand
from foodgram.settings import BASE_DIR
from recipes.models import MealTime

CSV_FILE_PATCH = os.path.join(BASE_DIR, 'data_csv/tags.csv')


class Command(BaseCommand):
    help = 'Load Tags'

    def handle(self, *args, **options):
        with open(CSV_FILE_PATCH, encoding='utf-8') as file:
            reader = csv.reader(file)
            for row in reader:
                name_english, name_russian = row
                (MealTime
                 .objects
                 .get_or_create(name_english=name_english,
                                name_russian=name_russian)
                 )
