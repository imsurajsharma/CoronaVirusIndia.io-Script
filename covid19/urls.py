from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path('', views.index),
    path('why/', views.whyUs),
    path('about/', views.aboutUs),
    path('contact/', views.contactUs),
    path('dash/',views.dashboard),
]