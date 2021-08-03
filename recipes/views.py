# from django.db.models.query import prefetch_related_objects
from django.shortcuts import render
from recipes.models import (Ingredient, Recipe,
                            RecipeIngredient, Subscription,
                            Favorite, )
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
# from django.db.models import Count
from django.core.paginator import Paginator
from recipes.utils import (get_recipes_full,
                           get_actual_tags)

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
        seted_tags_pk, tags = get_actual_tags(request.GET)
        recipes = (Recipe.objects
                   .filter(meal_time__in=seted_tags_pk)
                   .select_related('author')
                   .prefetch_related('meal_time')
                   .distinct()
                   )
        recipes = get_recipes_full(request, recipes)
        for recipe in recipes:
            print(f'recipe = {recipe}')
        paginator = Paginator(recipes, 3)
        page_number = request.GET.get('page')
        page = paginator.get_page(page_number)
        return render(request,
                      'recipes/index.html',
                      {'page': page, 'paginator': paginator,
                       'tags': tags}
                      )

    def view(request, recipe_id):
        recipe = get_object_or_404(Recipe, pk=recipe_id)
        ingredients = (RecipeIngredient.objects.select_related(
            'ingredient').filter(recipes=recipe))
        try:
            subscription = Subscription.objects.get(user=request.user,
                                                    author=recipe.author)
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

    @login_required
    def subscriptions(request):
        authors = User.objects.filter(subscription_author__user=request.user)
        print(f'authors = {authors}')
        recipes = Recipe.objects.filter(author__in=authors)
        return render(request,
                      'recipes/index.html',
                      {'recipes': recipes, }
                      )

    @login_required
    def favorites(request):
        seted_tags_pk, tags = get_actual_tags(request.GET)
        recipes = Recipe.objects.filter(favorite_recipe__user=request.user)
        recipes = get_recipes_full(request, recipes)
        paginator = Paginator(recipes, 3)
        page_number = request.GET.get('page')
        page = paginator.get_page(page_number)
        return render(request,
                      'recipes/favorite.html',
                      {'page': page, 'paginator': paginator,
                       'tags': tags})


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
