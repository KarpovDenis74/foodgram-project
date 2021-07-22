from django.shortcuts import render
from django.views.generic import ListView
from recipes.models import (Ingredient, Recipe)
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from recipes.serialisers import (IngredientSerializer,
                                 FormToRecipeSerializer)
# from django.db import transaction
from django.views.decorators.cache import cache_control, never_cache
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer
from time import sleep

User = get_user_model()


class RecipeViewList(ListView):
    template_name = 'recipes/index.html'
    model = Recipe


class RecipeView:
    def new(request):
        context = {'title': 'Создание рецепта',
                   'button_name': 'Создать рецепт'}
        if request.POST:
            recipe_form = FormToRecipeSerializer(request.POST)
            recipe_form.set_object_meal_time()
            print(
                f' - recipe_form.meal_time = {recipe_form.meal_time}')
            recipe_form.set_ingredient_and_amount()
            # if recipe_form.is_valid:
                # print(recipe_form)
                # print(f'- recipe_form.keys_post = {recipe_form.keys_post}')
            print(f'- recipe_form.ingredients = {recipe_form.ingredients}')
  

            return redirect('index')
            # render(request,
            #        'recipes/formRecipe.html',
            #        {'context': context, 'errors': recipe_form.errors})
        return render(request,
                      'recipes/formRecipe.html',
                      {'context': context})


class ApiIngredient(APIView):
    @api_view(('GET',))
    @renderer_classes((JSONRenderer,))
    def get(request):
        param = str(request.GET.get('query', None))
        if param is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        ingredient = Ingredient.objects.filter(title__icontains=param)
        serialiser = IngredientSerializer(ingredient, many=True)
        if serialiser.is_valid:
            return Response(serialiser.data, status=status.HTTP_200_OK)
        return Response(status=status.TTP_400_BAD_REQUEST)
