from django.urls import path
from . import views

urlpatterns = [
    path("", views.organisation_home, name="organisation_home"),
]
