"""
URL configuration for skyapp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views



urlpatterns = [
    path("", views.home, name="home"),  # Homepage
    path("admin/", admin.site.urls), # Django admin panel
    path('accounts/login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'), # MEMBER LOGIN 
    path('logout/',auth_views.LogoutView.as_view(template_name='logged_out.html',next_page=None),name='logout'), # LOGOUT
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='password_reset.html'),name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'),name='password_reset_done'),
    path('admin-login/',auth_views.LoginView.as_view(template_name='admin_login.html'),name='admin_login'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path("profile/", views.profile_view, name="profile"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("redirect-after-login/", views.redirect_after_login, name="redirect_after_login"),

    # App URLs
    path("teams/", include("teams.urls")),
    path("organisation/", include("organisation.urls")),
    path("messaging/", include("messaging.urls")),    
    path("schedule/", include("schedule.urls")),
    path("reports/", include("reports.urls")),
    path("visualisation/", include("visualisation.urls")),

]
