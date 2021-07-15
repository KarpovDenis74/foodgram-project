from django.shortcuts import render
from django.views.generic import ListView
from recipes.models import (Recipe,)
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from recipes.forms import RecipeForm


User = get_user_model()


class RecipeViewList(ListView):
    template_name = 'recipes/indexNotAuth.html'
    model = Recipe


class RecipeView:
    @login_required
    def new(request):
        context = {'title': 'Создание рецепта',
                   'button_name': 'Создать рецепт'}
        form = RecipeForm(request.POST or None,
                          files=request.FILES or None)
        if not form.is_valid():
            return render(request,
                          'recipes/formRecipe.html',
                          {'context': context, 'form': form}
                          )
        recipe = form.save(commit=False)
        recipe.author = request.user
        recipe.save()
        return redirect('resipes:index')
# def index(request):
#     return render(request, 'recipes/indexNotAuth.html'
#                   )
