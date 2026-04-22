"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from main import views 

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('', views.index_view, name='index'),
    path('home/', views.home_view, name='home'),
    path('catalog/', views.catalog_view, name='catalog'),
    path('orders/', views.orders_view, name='orders'),
    path('about/', views.about_view, name='about'),
    path('profile/', views.profile_view, name='profile'),
    path('selection/', views.selection_view, name='selection'),
    path('delivery/', views.delivery_view, name='delivery'),
    path('contacts/', views.contacts_view, name='contacts'),
    path('api/register/', views.register_user, name='register'),
    path('api/login/', views.login_user, name='login'),
    path('api/chat/', views.chat_api, name='chat_api'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
