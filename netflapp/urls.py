"""
URL configuration for netfl project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from . import views

urlpatterns = [
    path('json/',views.req),
    path('json/<str:host>/',views.req2),
    path('json/<str:host>/<int:loop>/',views.req2),
    path('json/<str:host>/<int:loop>/<int:sleep>',views.req2),
    path('<str:host>/',views.req),
    path('<str:host>/<int:loop>/',views.req),
    path('<str:host>/<int:loop>/<int:sleep>',views.req),
    path('',views.index),
]
