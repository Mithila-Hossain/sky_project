from django.urls import path
from .views import schedule_page, weekly_schedule, monthly_schedule, upcoming_schedule, create_meeting

app_name = "schedule"

urlpatterns = [
    path("", schedule_page, name="schedule_page"),
    path("weekly/", weekly_schedule, name="weekly_schedule"),
    path("monthly/", monthly_schedule, name="monthly_schedule"),
    path("upcoming/", upcoming_schedule, name="upcoming_schedule"),
    path("create/", create_meeting, name="create_meeting"),
]