from django.shortcuts import render
from recipes.models import (Ingredient, MealTime, Recipe,
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
# from django.db.models import Count
from django.core.paginator import Paginator
from recipes.utils import (get_recipes_full,
                           get_actual_tags)
from django.db.models import Count

User = get_user_model()


class RecipeView:
    @login_required
    def new(request):
        context = {'title': 'Создание рецепта',
                   'button_name': 'Создать рецепт',
                   'is_edit': False,
                   }
        if not request.POST:
            return render(request,
                          'recipes/formRecipe.html',
                          {'context': context,
                           'recipe_new_active': True})
        recipe_form = FormToRecipeSerializer(request)
        if not recipe_form.save():
            return render(request,
                          'recipes/formRecipe.html',
                          {'context': context,
                           'errors': recipe_form.errors,
                           'recipe_form': recipe_form,
                           'recipe_new_active': True})
        return redirect('index')

    def edit(request, recipe_id):
        recipe = get_object_or_404(Recipe, pk=recipe_id)
        meal_time = MealTime.objects.filter(rmt_mt__recipes=recipe.pk)
        meal_time_all = MealTime.objects.all()
        tags = []
        for tag in meal_time_all:
            if tag in meal_time:
                tags.append({'name': tag.name_english,
                             'enabled': True})
            else:
                tags.append({'name': tag.name_english,
                             'enabled': False})
        if recipe.author != request.user:
            return redirect('recipes:view_recipe', recipe_id=recipe_id)
        context = {'title': 'Редактирование рецепта',
                   'button_name': 'Сохранить',
                   'is_edit': True}
        ingredients = (RecipeIngredient.objects
                                       .filter(recipes=recipe)
                                       .select_related('ingredient'))
        # tags = MealTime.objects.filter(rmt_mt__recipes=recipe)
        file = request.FILES or None,
        if not request.POST:
            return render(request,
                          'recipes/formChangeRecipe.html',
                          {'context': context,
                           'recipe': recipe,
                           'ingredients': ingredients,
                           'file': file,
                           'tags': tags})
        recipe_form = FormToRecipeSerializer(request, recipe_id)
        if not recipe_form.save():
            return render(request,
                          'recipes/formChangeRecipe.html',
                          {'context': context,
                           'errors': recipe_form.errors,
                           'recipe_form': recipe_form,
                           'recipe': recipe})
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
        paginator = Paginator(recipes, 3)
        page_number = request.GET.get('page')
        page = paginator.get_page(page_number)
        return render(request,
                      'recipes/index.html',
                      {'page': page, 'paginator': paginator,
                       'tags': tags,
                       'index_active': True}
                      )

    def author(request, author_id):
        author = get_object_or_404(User, pk=author_id)
        seted_tags_pk, tags = get_actual_tags(request.GET)
        try:
            subscription = Subscription.objects.get(user=request.user,
                                                    author=author)
        except Exception:
            subscription = False
        recipes = (Recipe.objects
                   .filter(meal_time__in=seted_tags_pk,
                           author=author)
                   .select_related('author')
                   .prefetch_related('meal_time')
                   .distinct()
                   )
        recipes = get_recipes_full(request, recipes)
        paginator = Paginator(recipes, 1)
        page_number = request.GET.get('page')
        page = paginator.get_page(page_number)
        context = {'page': page, 'paginator': paginator,
                   'tags': tags,
                   'author': author,
                   'subscription': subscription}
        return render(request, 'recipes/authorRecipe.html', context)

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
        return render(request,
                      'recipes/singlePage.html',
                      {'recipe': recipe,
                       'ingredients': ingredients,
                       'subscription': subscription,
                       'favorite': favorite})

    @login_required
    def delete(request, recipe_id):
        recipe = get_object_or_404(Recipe, pk=recipe_id)
        if request.user != recipe.author:
            return redirect('recipes:view_recipe', recipe_id=recipe_id)
        context = {'title': 'Удаление рецепта',
                   'message': "Вы уверены, что хотите удалить рецепт?",
                   'recipe': recipe}
        if request.method != 'POST':
            return render(request, 'recipes/checkPage.html', context)
        Recipe.objects.get(pk=recipe_id).delete()
        return redirect('index')

    @login_required
    def subscriptions(request):
        author_recipes = []
        authors = (User
                   .objects
                   .filter(subscription_author__user=request.user)
                   .annotate(recipes_count=Count('recipe_author'))
                   )
        for author in authors:
            recipes = (Recipe
                       .objects
                       .filter(author=author)
                       )
            recipes_user_for_card = len(recipes)
            if recipes_user_for_card > 3:
                recipes = recipes[:3]
            else:
                recipes = recipes[:recipes_user_for_card]
            author_recipes.append([author,
                                   recipes,
                                   ])
        paginator = Paginator(author_recipes, 1)
        page_number = request.GET.get('page')
        page = paginator.get_page(page_number)
        return render(request,
                      'recipes/myFollow.html',
                      {'page': page,
                       'paginator': paginator,
                       }
                      )

    @login_required
    def favorites(request):
        seted_tags_pk, tags = get_actual_tags(request.GET)
        recipes = Recipe.objects.filter(favorite_recipe__user=request.user)
        recipes = get_recipes_full(request, recipes)
        paginator = Paginator(recipes, 1)
        page_number = request.GET.get('page')
        page = paginator.get_page(page_number)
        return render(request,
                      'recipes/favorite.html',
                      {'page': page, 'paginator': paginator,
                       'tags': tags,
                       'favorites_active': True})

    def shop_list(request):
        return render(request,
                      'recipes/favorite.html',
                      {'shop_list_active': True})


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
