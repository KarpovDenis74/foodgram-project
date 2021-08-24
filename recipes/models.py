from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import UniqueConstraint

User = get_user_model()


class MealTime(models.Model):
    name_english = models.CharField('Наименование на английском языке',
                                    max_length=128,
                                    blank=False,
                                    unique=True)
    name_russian = models.CharField('Наименование на русском языке',
                                    max_length=128,
                                    blank=False)

    def __str__(self):
        return self.name_english


class Ingredient(models.Model):
    title = models.CharField(max_length=256)
    dimension = models.CharField(max_length=128)

    def __str__(self):
        return f'{self.title}, {self.dimension}'

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        ordering = ('title', )


class Recipe(models.Model):
    name = models.CharField(max_length=128,
                            verbose_name='Название рецепта')
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='recipe_author',
                               verbose_name='Автор')
    text = models.TextField(
        verbose_name=('Описание рецепта'))
    time_cooking = (models.PositiveIntegerField(
                    validators=[MinValueValidator(1)],
                    verbose_name='Время приготовления,(в минутах)'))
    ingredient = models.ManyToManyField(Ingredient,
                                        through='RecipeIngredient',
                                        through_fields=('recipes',
                                                        'ingredient'),
                                        verbose_name='Ингредиент'
                                        )
    pub_date = models.DateTimeField(verbose_name='Дата публикации',
                                    auto_now_add=True,
                                    db_index=True)
    image = models.ImageField(upload_to='recipes/image/', blank=True,
                              verbose_name='Изображение готового блюда')
    slug = models.SlugField(max_length=150)
    meal_time = models.ManyToManyField(MealTime,
                                       related_name='rmt',
                                       through='RecipeMealTime',
                                       through_fields=('recipes',
                                                       'meal_time'),
                                       verbose_name='Время приема пищи'
                                       )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'


class RecipeMealTime(models.Model):
    recipes = models.ForeignKey(Recipe,
                                related_name='rmt_r',
                                on_delete=models.CASCADE)
    meal_time = models.ForeignKey(MealTime,
                                  related_name='rmt_mt',
                                  on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.recipes.name}: {self.meal_time.name_english}'

    class Meta:
        UniqueConstraint(fields=['recipes', 'meal_time'],
                         name='unique_recipes_meal_time')
        verbose_name = 'Период приема шищи'
        verbose_name_plural = 'Периоды приема пищи'
        ordering = ['-recipes']


class RecipeIngredient(models.Model):
    recipes = models.ForeignKey(Recipe,
                                on_delete=models.CASCADE,
                                related_name='recipe')
    ingredient = models.ForeignKey(Ingredient,
                                   on_delete=models.CASCADE,
                                   related_name='ingredient')
    amount = models.FloatField(verbose_name='Количество',
                               validators=[MinValueValidator(1)])

    def __str__(self):
        return f'{self.recipes.name}: {self.ingredient.title} - {self.amount}'

    class Meta:
        verbose_name = 'Ингредиент в рецепте'
        verbose_name_plural = 'Ингредиенты в рецептах'
        UniqueConstraint(fields=['recipes', 'ingredient'],
                         name='unique_recipes_ingredient')


class Favorite(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             verbose_name='Пользователь',
                             related_name='favorite_user')
    recipe = models.ForeignKey(Recipe,
                               on_delete=models.CASCADE,
                               verbose_name='Рецепт',
                               related_name='favorite_recipe')

    class Meta:
        UniqueConstraint(fields=['user', 'recipe'],
                         name='unique_favorite')
        verbose_name = 'Объект избранного'
        verbose_name_plural = 'Объекты избранного'


class Subscription(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             verbose_name='Пользователь',
                             related_name='subscription_user')
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               verbose_name='Рецепт',
                               related_name='subscription_author')

    class Meta:
        UniqueConstraint(fields=['user', 'author'],
                         name='unique_subscription')


class ShopList(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             verbose_name='Пользователь')
    recipe = models.ForeignKey(Recipe,
                               on_delete=models.CASCADE,
                               verbose_name='Рецепт')

    class Meta:
        UniqueConstraint(fields=['user', 'recipe'],
                         name='unique_shop_list')
