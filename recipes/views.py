from django.shortcuts import render
from django.utils.translation import ungettext
from django.views.generic import ListView
from recipes.models import (Ingredient, Recipe, 
                            RecipeIngredient, Subscription,
                            Favorite)
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from recipes.serialisers import (IngredientSerializer,
                                 FormToRecipeSerializer)
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer
from django.shortcuts import get_object_or_404

User = get_user_model()


class RecipeView:
    @login_required
    def new(request):
        context = {'title': 'Создание рецепта',
                   'button_name': 'Создать рецепт'}
        if not request.POST:
            return render(request,
                          'recipes/formRecipe.html',
                          {'context': context})
        recipe_form = FormToRecipeSerializer(request)
        if not recipe_form.save():
            return render(request,
                          'recipes/formRecipe.html',
                          {'context': context,
                           'errors': recipe_form.errors,
                           'recipe_form': recipe_form})
        return redirect('index')

    def list(request):
        recipes = Recipe.objects.all()
        return render(request,
                      'recipes/index.html',
                      {'recipes': recipes})

    def view(request, recipe_id):
        recipe = get_object_or_404(Recipe, pk=recipe_id)
        ingredients = RecipeIngredient.objects.select_related('ingredient').filter(recipes=recipe)
        try:
            subscription = Subscription.objects.get(user=request.user, author=recipe.author)
            subscription = 'on'
        except Exception:
            subscription = 'off'
        try:
            favorite = Favorite.objects.get(user=request.user, recipe=recipe)
            favorite = 'on'
        except Exception:
            favorite = 'off'
        print(f'favorite = {favorite}')
        return render(request,
                      'recipes/singlePage.html',
                      {'recipe': recipe,
                       'ingredients': ingredients,
                       'subscription': subscription,
                       'favorite': favorite})

    def subscriptions(request):
        recipes = get_object_or_404(Recipe, author=request.user)
        render(request,
               'recipes/singlePage.html',
               {'recipes': recipes,
                })



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
