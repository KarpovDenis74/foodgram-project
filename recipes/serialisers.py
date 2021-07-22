from rest_framework import serializers
from recipes.models import Recipe, Ingredient, MealTime
import re
from time import sleep


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
    def __init__(self, query, file):
        self.ingredients = []
        self.meal_time = []
        self.errors = []
        self.query = query
        self.description = self.query.get('description')
        self.name = self.query.get('name')[0]
        self.time_cooking = self.query.get('name')[1]
        self.image = file
        self.keys_post = self.query.keys()
        # маска ключа имени инградиента в POST-ответе
        self.name_ingredient_mask = 'nameIngredient_'
        # маска ключа количества инградиента в POST-ответе
        self.value_ingredient_mask = 'valueIngredient_'

    def is_valid(self):
        object_meal_time = self.set_object_meal_time()
        ingredient_and_amount = self.set_ingredient_and_amount()
        return True if (object_meal_time
                        and ingredient_and_amount) else False

    def set_object_meal_time(self):
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
            self.errors += ['Не правильно метки времени приема пищив']
            self.meal_time = False
            return bool(False)
        return bool(True)

    def set_ingredient_and_amount(self):
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
                ingredient_amount = int(self.query.get(
                    amount_ingredient_key))
                if ingredient_amount <= 0:
                    self.errors += ['Количество инградиентов'
                                    ' должно быть числом больше "0"']
                    return False
                ingredient_title = self.query.get(key)
                try:
                    ingredient_object = Ingredient.objects.get(
                        title=ingredient_title)
                    self.ingredients += [ingredient_object, ingredient_amount]
                except Exception:
                    pass
        if self.ingredients == []:
            self.ingredients = False
            self.errors += ['Инградиенты не найдены']
            return False
        return bool(True)
    
    def set_object_recipe_fields(self):
        return bool(True) 
