from django.urls import path
from . import views

urlpatterns = [
    path("", views.visualisation_home, name="visualisation_home"),
]
