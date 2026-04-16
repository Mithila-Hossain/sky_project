from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Team, TeamMember, Dependency, ContactChannel, Meeting
from messaging.models import Message
from django.utils import timezone


@login_required
def team_list(request):
    search_query = request.GET.get('search', '')

    if search_query:
        teams = Team.objects.filter(name__icontains=search_query)
    else:
        teams = Team.objects.all()

    return render(request, 'teams/team_list.html', {
        'teams': teams,
        'search_query': search_query,
    })


@login_required
def team_detail(request, team_id):
    team = get_object_or_404(Team, id=team_id)
    members = TeamMember.objects.filter(team=team)
    upstream = Dependency.objects.filter(downstream_team=team)
    downstream = Dependency.objects.filter(upstream_team=team)
    channels = ContactChannel.objects.filter(team=team)

    return render(request, 'teams/team_detail.html', {
        'team': team,
        'members': members,
        'upstream': upstream,
        'downstream': downstream,
        'channels': channels,
    })


@login_required
def email_team(request, team_id):
    team = get_object_or_404(Team, id=team_id)
    members = TeamMember.objects.filter(team=team)

    if request.method == 'POST':
        subject = request.POST.get('subject')
        body = request.POST.get('body')

        for member in members:
            Message.objects.create(
                subject=subject,
                body=body,
                sender=request.user,
                receiver=member.user,
                timeStamp=timezone.now(),
                status="Sent"
            )

        messages.success(request, "Email sent to all team members.")
        return redirect('team_detail', team_id=team.id)

    return render(request, 'teams/email_team.html', {'team': team})


@login_required
def schedule_meeting(request, team_id):
    team = get_object_or_404(Team, id=team_id)

    if request.method == 'POST':
        date_time = request.POST.get('date_time')
        platform = request.POST.get('platform')
        agenda = request.POST.get('agenda')
        schedule_type = request.POST.get('schedule_type')

        Meeting.objects.create(
            team=team,
            date_time=date_time,
            platform=platform,
            agenda=agenda,
            schedule_type=schedule_type
        )

        messages.success(request, "Meeting scheduled successfully.")
        return redirect('team_detail', team_id=team.id)

    return render(request, 'teams/schedule_meeting.html', {'team': team})
