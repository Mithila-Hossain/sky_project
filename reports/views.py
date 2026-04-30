from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from teams.models import Team, TeamMember
from organisation.models import Department

@login_required
def reports_view(request):

    total_teams = Team.objects.count()
    total_members = TeamMember.objects.count()
    total_depts = Department.objects.count()
   
    teams_no_manager = Team.objects.filter(manager__isnull=True) | Team.objects.filter(manager='')
    
    context = {
        'total_teams': total_teams,
        'total_members': total_members,
        'total_depts': total_depts,
        'teams_no_manager': teams_no_manager,
    }
    return render(request, 'reports.html', context)
