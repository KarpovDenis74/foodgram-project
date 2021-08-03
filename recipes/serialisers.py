from rest_framework import serializers
from recipes.models import Recipe, Ingredient, MealTime, RecipeIngredient
import re
from django.db import transaction


class MealTimeSerializer(serializers.ModelSerializer):
    name_english = serializers.CharField(max_length=128)

    class Meta:
        model = MealTime
        fields = ['name_english']


class RecipeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recipe
        fields = ['name', 'author', 'text',
                  'time_cooking', "pub_date", 'image',
                  'ingredient', 'miel_time']


class IngredientSerializer(serializers.ModelSerializer):
    title = serializers.CharField(max_length=256)
    dimension = serializers.CharField(max_length=128)

    class Meta:
        model = Ingredient
        fields = ['title', 'dimension']


class FormToRecipeSerializer:
    """
        Принимает в качестве аргумента словарь request.POST
        из POST запроса.
        сериализует полученные данные для объекта Recipe
        в переменные:
            self.ingredients = [объект Ingredient, amount]
            self.meal_time = [объекты MealTime}
    """
    def __init__(self, request):
        self.ingredients = []
        self.meal_time = []
        self.errors = {}
        self.request = request
        self.description = self.request.POST.get('description')
        self.name = self.request.POST.get('name')
        self.time_cooking = self.request.POST.get('time_cooking')
        self.image = ''
        self.keys_post = self.request.POST.keys()
        # маска ключа имени инградиента в POST-ответе
        self.name_ingredient_mask = 'nameIngredient_'
        # маска ключа количества инградиента в POST-ответе
        self.value_ingredient_mask = 'valueIngredient_'

    def meal_time_exist(self):
        """
        ищет объекты MealTime
        Результат действия:
            1. при наличии значений меток времени в модели MealTime:
                возвращает True
                устанавливает чписок найденных объектов:
                    self.meal_time = [ объект MealTime ]
            2. при их остсутствии:
                возвращает False
                self.meal_time = False
                self.errors += [текст ошибки] -с писок ошибок
        """
        try:
            for key in self.keys_post:
                meal_time_object = MealTime.objects.filter(
                    name_english=key)
                if meal_time_object.exists:
                    self.meal_time += meal_time_object
        except Exception:
            self.errors['meal_time'] = ('Поставте, пожалуста,'
                                        ' метки времени приема пищив')
            self.meal_time = False
            return bool(False)
        return bool(True)

    def ingredient_and_amount_exist(self):
        """
        ищет объект Ingredient и значение amount
        Ищет в ключах POST-запроса:
            - 'nameIngredient_' и 'valueIngredient_'
            - запрашивает данные в модели Ingredient
        Результат действия:
            1. при наличии значений ингредиентов в модели Ingredient:
                возвращает True
                устанавливает список найденных объектов:
                    self.ingredients = [объект Ingredient, amount]
                        # amount - количество ингредиента в рецепте
            2. при их остсутствии:
                возвращает False
                self.ingredients = False
                self.errors += [текст ошибки] -с писок ошибок
        """
        for key in self.keys_post:
            ingrgedient_mask_exist = re.search(self.name_ingredient_mask, key)
            if ingrgedient_mask_exist is not None:
                number_ingredient = re.findall(r'\d+', key)[0]
                amount_ingredient_key = ('valueIngredient_'
                                         f'{number_ingredient}')
                ingredient_amount = int(self.request.POST.get(
                    amount_ingredient_key))
                if ingredient_amount <= 0:
                    self.errors['amount'] = ('Количество инградиентов'
                                             ' должно быть числом больше "0"')
                    return False
                ingredient_title = self.request.POST.get(key)
                try:
                    ingredient_object = Ingredient.objects.get(
                        title=ingredient_title)
                    self.ingredients.append([ingredient_object,
                                            ingredient_amount])
                except Exception:
                    pass
        if self.ingredients == []:
            self.ingredients = False
            self.errors['ingredient'] = 'Инградиенты не найдены'
            return False
        return bool(True)

    def description_exist(self):
        if len(self.description) <= 0:
            self.errors['description'] = ('Пожалуйста, опишите Ваш рецепт')
            return bool(False)
        return bool(True)

    def name_exist(self):
        if (len(self.name) < 1 or len(self.name) >= 128):
            self.errors['name'] = ('Дайте рецепту название'
                                   ' - не больше 128 символов')
            return bool(False)
        return bool(True)

    def time_cooking_exist(self):
        try:
            self.time_cooking = int(self.time_cooking)
        except Exception:
            self.errors['time_cooking'] = (
                'Время приготовления должно быть числом')
            return bool(False)
        if self.time_cooking <= 0:
            self.errors['time_cooking'] = (
                'Время приготовления должно быть положительным числом')
            return bool(False)
        return bool(True)

    def image_exist(self):
        try:
            self.image = self.request.FILES.get('file')
        except Exception:
            self.image = None
        return bool(True)

    def save(self):
        if not (self.name_exist()
                and self.meal_time_exist()
                and self.ingredient_and_amount_exist()
                and self.time_cooking_exist()
                and self.description_exist()
                and self.image_exist()):
            return bool(False)
        try:
            with transaction.atomic():
                recipe = Recipe(name=self.name,
                                author=self.request.user,
                                text=self.description,
                                time_cooking=self.time_cooking,
                                image=self.image)
                recipe.save()
                print('рецепт сохранен')
                for meal_time in self.meal_time:
                    recipe.meal_time.add(meal_time)
                print(' тэги сохранены')
                for ingr_number in range(0, len(self.ingredients)):
                    recipe_ingredient = RecipeIngredient(
                        recipes=recipe,
                        ingredient=self.ingredients[ingr_number][0],
                        amount=self.ingredients[ingr_number][1])
                    recipe_ingredient.save()
                print(' инградиенты  сохранены')
        except Exception:
            self.errors['form_error'] = (
                'Рецепт не может быть сохранен.'
                ' Заполните, пожалуста, данные формы.')
            print(self.errors)
            return bool(False)
        return bool(True)
