# Author: Bernard Vecino w19733959

from django.urls import path
from . import views

urlpatterns = [
    path("", views.organisation_home, name="organisation_home"),
    path('departments/<int:dept_id>/', views.department_detail, name='department_detail'),
]
