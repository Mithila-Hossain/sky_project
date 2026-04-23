from django.urls import path
from . import views

urlpatterns = [
    # This makes the page available at /reports/
    path('', views.report_home_view, name='report_page'),
]