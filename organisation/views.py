# Author: Bernard Vecino w19733959

from django.shortcuts import render
from django.http import HttpResponse
from .models import Department
from teams.models import Dependency, Team

# Create your views here.

def organisation_home(request):
    departments = Department.objects.all()
    dependencies = Dependency.objects.all() 
    teams = Team.objects.all()

    context = {
        "departments": departments,
        "dependencies": dependencies,
        "teams": teams,
        "page_title": "Organisation",
        "calendar_title": "Team Connections"
    }

    return render(request, "organisation\organisation.html", context)

def department_detail(request, dept_id):
    department = Department.objects.get(id=dept_id)
    teams = Team.objects.filter(department_id=dept_id)
    return render(request, "organisation\department_detail.html", {
        "department": department,
        "teams": teams
        })
