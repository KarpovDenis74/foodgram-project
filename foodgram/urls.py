from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from recipes import views
# from rest_framework.routers import DefaultRouter
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import handler404, handler500

handler404 = "users.views.page_not_found"  # noqa
handler500 = "users.views.server_error"  # noqa

urlpatterns = [
    path('api/', include("api.urls")),
    path('admin/', admin.site.urls),
    path('users/', include("users.urls")),
    path('captcha/', include('captcha.urls')),
    path('', include("recipes.urls")),
    path('', views.RecipeView.list, name="index"),
]
if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [

        path('__debug__/', include(debug_toolbar.urls)),
    ]
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
