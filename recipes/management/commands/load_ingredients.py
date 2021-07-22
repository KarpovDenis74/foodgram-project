from django.core.management.base import BaseCommand
# from django.core.management.base import CommandError
from recipes.models import Ingredient
import csv
from foodgram.settings import BASE_DIR
import os

CSV_FILE_PATCH = os.path.join(BASE_DIR, 'ingredients.csv')


class Command(BaseCommand):
    help = 'Load Ingredient'

    def handle(self, *args, **options):
        with open(CSV_FILE_PATCH, encoding='utf-8') as file:
            reader = csv.reader(file)
            for row in reader:
                title, dimension = row
                Ingredient.objects.get_or_create(
                    title=title, dimension=dimension)
