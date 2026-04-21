from datetime import timedelta
from django.shortcuts import render, redirect
from django.utils import timezone
from teams.models import Meeting, Team


# ALL MEETINGS
def schedule_page(request):
    meetings = Meeting.objects.all().order_by("date_time")
    return render(request, "schedule/schedule_page.html", {
        "meetings": meetings,
        "page_title": "All Meetings"
    })


# WEEKLY
def weekly_schedule(request):
    today = timezone.now()
    week_later = today + timedelta(days=7)

    meetings = Meeting.objects.filter(
        date_time__range=[today, week_later]
    ).order_by("date_time")

    return render(request, "schedule/schedule_page.html", {
        "meetings": meetings,
        "page_title": "Weekly Schedule"
    })


# MONTHLY
def monthly_schedule(request):
    today = timezone.now()
    month_later = today + timedelta(days=30)

    meetings = Meeting.objects.filter(
        date_time__range=[today, month_later]
    ).order_by("date_time")

    return render(request, "schedule/schedule_page.html", {
        "meetings": meetings,
        "page_title": "Monthly Schedule"
    })


# UPCOMING (future only)
def upcoming_schedule(request):
    meetings = Meeting.objects.filter(
        date_time__gte=timezone.now()
    ).order_by("date_time")

    return render(request, "schedule/schedule_page.html", {
        "meetings": meetings,
        "page_title": "Upcoming Schedule"
    })


# CREATE MEETING (simple version for now)
def create_meeting(request):
    return render(request, "schedule/create_meeting.html")