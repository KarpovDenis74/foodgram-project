from django.db import models
from django.contrib.auth import get_user_model
from django.db.models import constraints
from django.forms import fields
from django.core.validators import MinValueValidator
# from django.db.models.aggregates import Count

User = get_user_model()


class Ingredient(models.Model):
    title = models.CharField(max_length=256)
    unit = models.CharField(max_length=128)

    def __str__(self):
        return f'{self.title}, {self.unit}'

#    class Meta(self):


class Recipe(models.Model):
    name = models.CharField(max_length=256,
                            verbose_name='Название рецепта')
    author = models.ForeignKey(User, 
                               on_delete=models.CASCADE,
                               related_name='recipe',
                               verbose_name='Автор')
    text = models.TextField()
    time_cooking = models.PositiveIntegerField(verbose_name='Время приготовления')
    ingredient = models.ManyToManyField(Ingredient, 
                                        through="RecipeIngredient",
                                        through_fields=('recipes',
                                                        'ingredient')
    )
    pub_date = models.DateTimeField(verbose_name='Дата публикации',
                                    auto_now_add=True,
                                    db_index=True)
    image = models.ImageField(upload_to='posts/', blank=True, 
                              verbose_name='Изображение готового блюда')

    def __str__(self):
        return self.title


    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'


class RecipeIngredient(models.Model):
    recipes = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    count = models.FloatField(verbose_name="Количество",
                              validators=[MinValueValidator(0)])

    def __str__(self):
        return f'{self.recipes.title}: {self.ingredient.title}: {self.count}'

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
        constraints = [
                       models.UniqueConstraint(
                        fields = ('user', 'recipe'),
                        name = 'unique_favorite_user_recipe'
        )]
        verbose_name = 'Объект избранного'
        verbose_name_plural = 'Объекты избранного'
