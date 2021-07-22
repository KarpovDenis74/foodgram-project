from django.urls import path
# from django.urls.conf import include
from recipes import views

app_name = 'recipes'

urlpatterns = [
    path('new/', views.RecipeView.new, name="new"),
]
