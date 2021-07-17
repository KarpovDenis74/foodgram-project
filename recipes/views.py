from django.shortcuts import render
from django.views.generic import ListView
from recipes.models import (Ingredient, Recipe,)
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from recipes.forms import RecipeForm
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from recipes.serialisers import IngredientSerializer


User = get_user_model()


class RecipeViewList(ListView):
    template_name = 'recipes/index.html'
    model = Recipe


class RecipeView:
    @login_required
    def new(request):
        context = {'title': 'Создание рецепта',
                   'button_name': 'Создать рецепт'}
        form = RecipeForm(request.POST or None,
                          files=request.FILES or None)
        if request.POST:
            if not form.is_valid():
                return render(request,
                            'recipes/formRecipe.html',
                            {'context': context, 'form': form}
                            )
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.save()
            return redirect('index')
        return render(request,
                      'recipes/formRecipe.html',
                      {'context': context, 'form': form}
                      )


class ApiIngredient(APIView):
    def get(self, request):
        param = request.GET.get('query', None)
        if param is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        ingredient = Ingredient.objects.filter(title__iexact=param)
        serialiser = IngredientSerializer(ingredient)
        return Response(serialiser.data, status=status.HTTP_200_OK)
        
# def index(request):
#     return render(request, 'recipes/indexNotAuth.html'
#                   )
