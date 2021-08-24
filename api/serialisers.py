from recipes.models import Ingredient
from rest_framework import serializers


class IngredientSerializer(serializers.ModelSerializer):
    title = serializers.CharField(max_length=256)
    dimension = serializers.CharField(max_length=128)

    class Meta:
        model = Ingredient
        fields = ['title', 'dimension']
