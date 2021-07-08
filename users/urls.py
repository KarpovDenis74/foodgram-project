from django.urls import path
from users import views
from django.contrib.auth import get_user_model
from django.urls.conf import include

User = get_user_model()

urlpatterns = [
    path("auth/signup/", views.SignUp.as_view(), name="signup"),
    path("auth/", include("django.contrib.auth.urls")),
    path('captcha/', include('captcha.urls')),
    path('users_admin/', views.users_admin, name='users_admin'),
    path('users_admin_edit/<int:user_id>/',
         views.users_admin_edit, name='users_admin_edit'),
    path('users_admin_delete/<int:user_id>/',
         views.users_admin_delete, name='users_admin_delete'),
]
