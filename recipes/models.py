from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.forms.widgets import MediaDefiningClass
# from django.db.models.aggregates import Count

User = get_user_model()


class Ingredient(models.Model):
    title = models.CharField(max_length=256)
    dimension = models.CharField(max_length=128)

    def __str__(self):
        return f'{self.title}, {self.unit}'
    
    class Meta:
        verbose_name = 'Инградиент'
        verbose_name_plural = 'Инградиенты'
        ordering = ('title', )

#    class Meta(self):


class Recipe(models.Model):
    name = models.CharField(max_length=128,
                            verbose_name='Название рецепта')
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='recipe',
                               verbose_name='Автор')
    text = models.TextField(
        verbose_name=('Описание рецепта'))
    time_cooking = (models.PositiveIntegerField(
                    verbose_name='Время приготовления,(в минутах)'))
    ingredient = models.ManyToManyField(Ingredient,
                                        through="RecipeIngredient",
                                        through_fields=('recipes',
                                                        'ingredient'),
                                        verbose_name='Инградиент'
                                        )
    pub_date = models.DateTimeField(verbose_name='Дата публикации',
                                    auto_now_add=True,
                                    db_index=True)
    image = models.ImageField(upload_to='recipes/image/', blank=True,
                              verbose_name='Изображение готового блюда')
    slug =  models.SlugField(max_length=150)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'


class RecipeIngredient(models.Model):
    recipes = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    amount = models.FloatField(verbose_name="Количество",
                              validators=[MinValueValidator(0)])

    def __str__(self):
        return f'{self.recipes.name}: {self.ingredient.title} - {self.amount}'

    class Meta:
        verbose_name = 'Инградиент в рецепте'
        verbose_name_plural = 'Инградиенты в рецептах'


class Favorite(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             verbose_name='Пользователь',
                             related_name='favorite')
    recipe = models.ForeignKey(Recipe,
                               on_delete=models.CASCADE,
                               verbose_name='Рецепт',
                               related_name='favorite')

    class Meta:
        constraints = ([models.UniqueConstraint(
                       fields=('user', 'recipe'),
                       name='unique_favorite_user_recipe',
                       )])
        verbose_name = 'Объект избранного'
        verbose_name_plural = 'Объекты избранного'
