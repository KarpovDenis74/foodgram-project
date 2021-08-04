from django.urls import path
# from django.urls.conf import include
from recipes import views

app_name = 'recipes'

urlpatterns = [
    path('', views.RecipeView.list, name="index"),
    path('recipes/new/', views.RecipeView.new, name="new"),
    path('recipes/<int:recipe_id>/edit/', views.RecipeView.edit,
         name="edit_recipe"),
    path('recipes/<int:recipe_id>/', views.RecipeView.view,
         name="view_recipe"),
    path('recipes/subscriptions/',
         views.RecipeView.subscriptions, name="subscriptions"),
    path('recipes/favorites/',
         views.RecipeView.favorites, name="favorites"),
]
