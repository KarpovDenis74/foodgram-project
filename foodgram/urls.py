from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from recipes import views
# from rest_framework.routers import DefaultRouter
from django.conf import settings


urlpatterns = [
    path('api/v1/ingredients/', views.ApiIngredient.get,
         name="api_ingredients"),
    path('admin/', admin.site.urls),
    path('users/', include("users.urls")),
    path('recipes/', include("recipes.urls")),
    path('', views.RecipeViewList.as_view(), name="index"),
]
if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [

        path('__debug__/', include(debug_toolbar.urls)),
    ]
