"""SemaLynx URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from .views import index  
from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path("simple_function", views.simple_function),
    path("simple_function2", views.simple_function2),
    path("simple_function3", views.simple_function3),
    path("machine_info", views.machine_info),
    path("machine_info2", views.machine_info2),
    path("machine_info3", views.machine_info3),
]
