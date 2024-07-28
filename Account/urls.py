from django.urls import path, re_path

from .views import CustomTokenCreateView, CustomTokenDestroyView, UpdateAccountView

urlpatterns = [
    re_path(r"^token/login/?$", CustomTokenCreateView.as_view()),
    re_path(r"^token/logout/?$", CustomTokenDestroyView.as_view()),
    path('users/me/', UpdateAccountView.as_view()),
]
