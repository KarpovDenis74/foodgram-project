from django.urls import path
from api import views

app_name = 'api'

urlpatterns = [
    path('v1/ingredients/', views.Api.get_ingredients,
         name="get_ingredients"),
    path('v1/subscriptions/<int:author_id>/', views.Api.set_subscriptions,
         name="subscriptions"),
    path('v1/favorites/<int:recipe_id>/', views.Api.set_favorites,
         name="favorites"),
    path('v1/purchases/<int:recipe_id>/', views.Api.set_purchases,
         name="purchases"),
]
