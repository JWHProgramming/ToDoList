from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path("register", views.register),
    path("home", views.home),
    path("login", views.login),
    path("logout", views.logout),
    path("add", views.add),
    path("complete/<int:id>", views.complete_toggle),
]