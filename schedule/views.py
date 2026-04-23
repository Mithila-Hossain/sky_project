from datetime import timedelta
from django.shortcuts import render, redirect
from django.utils import timezone
from teams.models import Meeting, Team


def schedule_page(request):
    meetings = Meeting.objects.all().order_by("date_time")
    upcoming_meetings = meetings[:5]
    teams = Team.objects.all()

    return render(request, "schedule/schedule_page.html", {
        "meetings": meetings,
        "upcoming_meetings": upcoming_meetings,
        "teams": teams,
        "page_title": "All Meetings",
        "calendar_title": "All Schedule"
    })


def weekly_schedule(request):
    today = timezone.now()
    week_later = today + timedelta(days=7)

    meetings = Meeting.objects.filter(
        date_time__range=[today, week_later]
    ).order_by("date_time")

    upcoming_meetings = meetings[:5]
    teams = Team.objects.all()

    return render(request, "schedule/schedule_page.html", {
        "meetings": meetings,
        "upcoming_meetings": upcoming_meetings,
        "teams": teams,
        "page_title": "Weekly Schedule",
        "calendar_title": "This Week"
    })


def monthly_schedule(request):
    today = timezone.now()
    month_later = today + timedelta(days=30)

    meetings = Meeting.objects.filter(
        date_time__range=[today, month_later]
    ).order_by("date_time")

    upcoming_meetings = meetings[:5]
    teams = Team.objects.all()

    return render(request, "schedule/schedule_page.html", {
        "meetings": meetings,
        "upcoming_meetings": upcoming_meetings,
        "teams": teams,
        "page_title": "Monthly Schedule",
        "calendar_title": "This Month"
    })


def upcoming_schedule(request):
    meetings = Meeting.objects.filter(
        date_time__gte=timezone.now()
    ).order_by("date_time")

    upcoming_meetings = meetings[:5]
    teams = Team.objects.all()

    return render(request, "schedule/schedule_page.html", {
        "meetings": meetings,
        "upcoming_meetings": upcoming_meetings,
        "teams": teams,
        "page_title": "Upcoming Schedule",
        "calendar_title": "Upcoming Meetings"
    })


def create_meeting(request):
    if request.method == "POST":
        team_id = request.POST.get("team")
        date_time = request.POST.get("date_time")
        platform = request.POST.get("platform")
        schedule_type = request.POST.get("schedule_type")
        agenda = request.POST.get("agenda")

        if team_id and date_time and platform and schedule_type:
            team = Team.objects.get(id=team_id)

            Meeting.objects.create(
                team=team,
                date_time=date_time,
                platform=platform,
                schedule_type=schedule_type,
                agenda=agenda
            )

    return redirect("schedule:schedule_page")