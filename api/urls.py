from django.urls import path

from api import views

app_name = 'api'

urlpatterns = [
    path('ingredients/', views.Api.get_ingredients,
         name='get_ingredients'),
    path('subscriptions/<int:author_id>/', views.Api.set_subscriptions,
         name='subscriptions'),
    path('favorites/<int:recipe_id>/', views.Api.set_favorites,
         name='favorites'),
    path('purchases/<int:recipe_id>/', views.Api.set_purchases,
         name='purchases'),
]
