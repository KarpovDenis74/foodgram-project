from rest_framework import serializers
from recipes.models import Recipe, Ingredient

class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ['name', 'author', 'text', 'time_cooking', "pub_date"]


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ['title', 'dimension']
