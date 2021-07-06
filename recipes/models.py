from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.aggregates import Count

User = get_user_model()

class Ingredient(models.Model):
    title = models.CharField(max_length=256)
    unit = models.CharField(max_length=128)

    def ___str__(self):
        return f'{self.title}, {self.unit}'

#    class Meta(self):

class Recipe(models.Model):
    title = models.CharField(max_length=256)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    time_cooking = models.PositiveIntegerField()
    ingredient = models.ManyToManyField(Ingredient, through="RecipeIngredient")

    def __str__(self):
        return self.title


class RecipeIngredient(models.Model):
    recipes = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    count = models.PositiveIntegerField()

    def __str__(self) -> str:
        return f'{self.recipes.title}, {self.ingredient.title}: {self.count}'
