from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test, login_required
from teams.models import Team


# Homepage (keep this)
def home(request):
    return render(request, 'home.html')

# User Dashboard
@login_required
def dashboard(request):
    return render(request, "home.html")


# Redirect After Login
@login_required
def redirect_after_login(request):
    if request.user.is_staff or request.user.is_superuser:
        return redirect('admin_dashboard')
    return redirect('dashboard')


# Helper: check if user is admin/staff
def is_admin(user):
    return user.is_staff or user.is_superuser


# Admin Dashboard View
@user_passes_test(is_admin)
def admin_dashboard(request):

    teams = Team.objects.all()

    context = {
        "total_teams": teams.count(),
        "active_projects": 156,
        "pending_issues": 24,
        "updates_today": 12,

        "recent_activities": [
            {"title": "New team member added to Frontend Development", "time": "2 hours ago"},
            {"title": "Backend Services team details updated", "time": "5 hours ago"},
        ],

        "teams": teams,
    }

    return render(request, "admin_dashboard.html", context)


# Profile Page View (ADD THIS)
@login_required
def profile_view(request):
    user = request.user

    profile = {
        "role": "Team Member",
        "department_name": "Not assigned",
        "location": "Not specified",
        "preferred_contact": "Email",
        "notifications_text": "Enabled for important updates",
    }

    context = {
        "user": user,
        "profile": profile,
    }

    return render(request, "profile.html", context)
