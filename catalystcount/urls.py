"""
URL configuration for catalystcount project.

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
from django.contrib import admin
from django.urls import path,include
from catalystcountapp import views
urlpatterns = [
    path("admin/", admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path("welcome/",views.homepagedata),
    path('upload/', views.upload_file, name='upload_file'),
    path('query_builder/', views.query_builder, name='query_builder'),
    path('api/query_companies/', views.query_companies, name='query_companies'),
    path('users/', views.users_list, name='users_list'),
    path('add_user/', views.add_user, name='add_user'),
    path('delete_user/<int:user_id>/',views.delete_user, name='delete_user'),
    path("",views.home)
]



