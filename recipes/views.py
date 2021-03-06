# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Count, Sum
from django.http import FileResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic.base import TemplateView
from rest_framework import status
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from recipes.models import Ingredient, MealTime, Recipe, RecipeIngredient
from recipes.serialisers import FormToRecipeSerializer, IngredientSerializer
from recipes.utils import (get_actual_tags, get_favorite, get_pdf,
                           get_recipes_full, get_shop_list,
                           get_shop_list_count, get_subscription)

User = get_user_model()


class RecipeView:
    @login_required
    def new(request):
        shop_list_count = get_shop_list_count(request)
        context = {'title': 'Создание рецепта',
                   'button_name': 'Создать рецепт',
                   'is_edit': False,
                   }
        if not request.POST:
            return render(request,
                          'recipes/formRecipe.html',
                          {'context': context,
                           'recipe_new_active': True,
                           'shop_list_count': shop_list_count})
        recipe_form = FormToRecipeSerializer(request)
        if not recipe_form.save():
            return render(request,
                          'recipes/formRecipe.html',
                          {'context': context,
                           'errors': recipe_form.errors,
                           'recipe_form': recipe_form,
                           'recipe_new_active': True,
                           'shop_list_count': shop_list_count})
        return redirect('index')

    @login_required
    def edit(request, recipe_id):
        recipe = get_object_or_404(Recipe, pk=recipe_id)
        shop_list_count = get_shop_list_count(request)
        meal_time = MealTime.objects.filter(rmt_mt__recipes=recipe.pk)
        meal_time_all = MealTime.objects.all()
        tags = []
        for tag in meal_time_all:
            tags.append({'name': tag.name_english,
                         'enabled': tag in meal_time})
        if recipe.author != request.user:
            return redirect('recipes:view_recipe', recipe_id=recipe_id)
        context = {'title': 'Редактирование рецепта',
                   'button_name': 'Сохранить',
                   'is_edit': True}
        ingredients = (RecipeIngredient.objects
                                       .filter(recipes=recipe)
                                       .select_related('ingredient'))
        file = request.FILES or None,
        if not request.POST:
            return render(request,
                          'recipes/formChangeRecipe.html',
                          {'context': context,
                           'recipe': recipe,
                           'ingredients': ingredients,
                           'file': file,
                           'tags': tags,
                           'shop_list_count': shop_list_count})
        recipe_form = FormToRecipeSerializer(request, recipe_id)
        if not recipe_form.save():
            return render(request,
                          'recipes/formChangeRecipe.html',
                          {'context': context,
                           'errors': recipe_form.errors,
                           'recipe_form': recipe_form,
                           'recipe': recipe,
                           'shop_list_count': shop_list_count})
        return redirect('index')

    def list(request):
        shop_list_count = get_shop_list_count(request)
        seted_tags_pk, tags = get_actual_tags(request.GET)
        recipes = (Recipe.objects
                   .filter(meal_time__in=seted_tags_pk)
                   .select_related('author')
                   .prefetch_related('meal_time')
                   .distinct()
                   )
        recipes = get_recipes_full(request, recipes)
        paginator = Paginator(recipes, settings.RECIPE_IN_PAGE)
        page_number = request.GET.get('page')
        page = paginator.get_page(page_number)
        return render(request,
                      'recipes/index.html',
                      {'page': page, 'paginator': paginator,
                       'tags': tags,
                       'index_active': True,
                       'shop_list_count': shop_list_count}
                      )

    def author(request, author_id):
        author = get_object_or_404(User, pk=author_id)
        shop_list_count = get_shop_list_count(request)
        seted_tags_pk, tags = get_actual_tags(request.GET)
        subscription = get_subscription(request, author)
        recipes = (Recipe.objects
                   .filter(meal_time__in=seted_tags_pk,
                           author=author)
                   .select_related('author')
                   .prefetch_related('meal_time')
                   .distinct()
                   )
        recipes = get_recipes_full(request, recipes)
        paginator = Paginator(recipes, settings.RECIPE_IN_PAGE)
        page_number = request.GET.get('page')
        page = paginator.get_page(page_number)
        context = {'page': page, 'paginator': paginator,
                   'tags': tags,
                   'author': author,
                   'subscription': subscription,
                   'shop_list_count': shop_list_count}
        return render(request, 'recipes/authorRecipe.html', context)

    def view(request, recipe_id):
        recipe = get_object_or_404(Recipe, pk=recipe_id)
        shop_list_count = get_shop_list_count(request)
        ingredients = (RecipeIngredient.objects.select_related(
            'ingredient').filter(recipes=recipe))
        subscription = get_subscription(request, recipe.author)
        favorite = get_favorite(request, recipe)
        shop_list = get_shop_list(request, recipe)
        return render(request,
                      'recipes/singlePage.html',
                      {'recipe': recipe,
                       'ingredients': ingredients,
                       'subscription': subscription,
                       'favorite': favorite,
                       'shop_list_count': shop_list_count,
                       'shop_list': shop_list})

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
        recipe.delete()
        return redirect('index')

    @login_required
    def subscriptions(request):
        author_recipes = []
        shop_list_count = get_shop_list_count(request)
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
            if recipes_user_for_card > settings.RECIPE_IN_PAGE:
                recipes = recipes[:settings.RECIPE_IN_PAGE]
            else:
                recipes = recipes[:recipes_user_for_card]
            author_recipes.append([author,
                                   recipes,
                                   ])
        paginator = Paginator(author_recipes, settings.RECIPE_IN_PAGE)
        page_number = request.GET.get('page')
        page = paginator.get_page(page_number)
        return render(request,
                      'recipes/myFollow.html',
                      {'page': page,
                       'paginator': paginator,
                       'shop_list_count': shop_list_count
                       }
                      )

    @login_required
    def favorites(request):
        shop_list_count = get_shop_list_count(request)
        seted_tags_pk, tags = get_actual_tags(request.GET)
        recipes = (Recipe.objects.filter(meal_time__in=seted_tags_pk,
                                         favorite_recipe__user=request.user)
                   .distinct())
        recipes = get_recipes_full(request, recipes)
        paginator = Paginator(recipes, settings.RECIPE_IN_PAGE)
        page_number = request.GET.get('page')
        page = paginator.get_page(page_number)
        return render(request,
                      'recipes/favorite.html',
                      {'page': page, 'paginator': paginator,
                       'tags': tags,
                       'favorites_active': True,
                       'shop_list_count': shop_list_count})

    def shop_list(request):
        if request.user.is_authenticated:
            recipes = Recipe.objects.filter(shoplist__user=request.user)
        elif request.session.get('purchases'):
            recipes = (Recipe
                       .objects
                       .filter(pk__in=request.session['purchases']))
        else:
            recipes = None
        shop_list_count = get_shop_list_count(request)
        return render(request,
                      'recipes/shopList.html',
                      {'shop_list_active': True,
                       'recipes': recipes,
                       'shop_list_count': shop_list_count})

    def download_shop_list(request):
        if request.user.is_authenticated:
            ingr = (Ingredient
                    .objects
                    .filter(ingredient__recipes__shoplist__user=request.user)
                    .annotate(count=Sum('ingredient__amount'))
                    )
        else:
            ingr = (Ingredient
                    .objects
                    .filter(ingredient__recipes__in=(request
                                                     .session['purchases']))
                    .annotate(count=Sum('ingredient__amount'))
                    )
        buffer = get_pdf(ingr)
        return FileResponse(buffer, as_attachment=True,
                            filename='shoplist.pdf')


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


class AuthorPage(TemplateView):
    template_name = 'recipes/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Об авторе'
        return context


class TeсhnologiesPage(TemplateView):
    template_name = 'recipes/teсhnologies.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Используемый стек технологий'
        return context
