"""
URL configuration for AlgoViz project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from AlgoViz import settings
from .views import HomeView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('tinymce/', include('tinymce.urls')),

    path('api/auth/', include('djoser.urls')),
    # path('api/auth/', include('djoser.urls.authtoken')),
    path('api/auth/', include('Account.urls')),

    path('api/', include('Account.urls')),
    path('api/algorithms/', include('Algorithm.urls')),

    path('', HomeView.as_view(), {'resource': ''}),
    path('<path:resource>', HomeView.as_view())
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
