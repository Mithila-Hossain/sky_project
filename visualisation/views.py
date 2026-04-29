from django.shortcuts import render
from django.db.models import Count
from django.db.models.functions import TruncDate

from bokeh.plotting import figure
from bokeh.embed import components

from organisation.models import Department
from teams.models import Team, TeamMember, Dependency, Meeting


def visualisation_home(request):
    teams_queryset = Team.objects.all()

    # first chart: department vs teams
    department_data = (
        Department.objects
        .annotate(team_count=Count("team"))
        .order_by("name")
    )

    department_names = [department.name for department in department_data]
    team_counts = [department.team_count for department in department_data]

    if not department_names:
        department_names = ["No data"]
        team_counts = [0]

    main_chart = figure(
        title="Teams / Projects by Department",
        x_range=department_names,
        x_axis_label="Department",
        y_axis_label="Number of Teams / Projects",
        height=350,
        sizing_mode="stretch_width",
        toolbar_location=None
    )

    main_chart.vbar(
        x=department_names,
        top=team_counts,
        width=0.6
    )

    main_chart.xaxis.major_label_orientation = 0.8

    # second chart: team size breakdown
    team_data = (
        Team.objects
        .annotate(member_count=Count("members"))
        .order_by("name")
    )

    team_names = [team.name for team in team_data]
    member_counts = [team.member_count for team in team_data]

    if not team_names:
        team_names = ["No data"]
        member_counts = [0]

    category_chart = figure(
        title="Team Size (Members per Team)",
        x_range=team_names,
        x_axis_label="Team",
        y_axis_label="Number of Members",
        height=350,
        sizing_mode="stretch_width",
        toolbar_location=None
    )

    category_chart.vbar(
        x=team_names,
        top=member_counts,
        width=0.6
    )

    category_chart.xaxis.major_label_orientation = 0.8

    # third chart: employee distribution by department
    employee_data = (
        Department.objects
        .annotate(employee_count=Count("team__members"))
        .order_by("name")
    )

    department_labels = []
    employee_counts = []

    for department in employee_data:
        if department.employee_count > 0:
            department_labels.append(department.name)
            employee_counts.append(department.employee_count)

    if not department_labels:
        department_labels = ["No Data"]
        employee_counts = [1]

    created_data = (
    Team.objects
    .annotate(created_date=TruncDate("created_at"))
    .values("created_date")
    .annotate(team_count=Count("id"))
    .order_by("created_date")
    )

    created_dates = [str(item["created_date"]) for item in created_data]
    created_counts = [item["team_count"] for item in created_data]

    if not created_dates:
        created_dates = ["No data"]
        created_counts = [0]

    time_chart = figure(
        title="Teams Created Over Time",
        x_range=created_dates,
        x_axis_label="Date Created",
        y_axis_label="Number of Teams",
        height=350,
        sizing_mode="stretch_width",
        toolbar_location=None
    )

    # line
    time_chart.line(
        x=created_dates,
        y=created_counts,
        line_width=3
    )

    # points
    time_chart.circle(
        x=created_dates,
        y=created_counts,
        size=8
    )

    time_chart.xaxis.major_label_orientation = 0.8

    # recent data summary table
    recent_teams = (
        teams_queryset
        .select_related("department", "team_leader", "project")
        .order_by("-created_at")[:5]
    )

    # bokeh components for chart 1, 2 and 4
    main_script, main_div = components(main_chart)
    category_script, category_div = components(category_chart)
    time_script, time_div = components(time_chart)

    context = {
        "main_script": main_script,
        "main_div": main_div,

        "category_script": category_script,
        "category_div": category_div,

        "department_labels": department_labels,
        "employee_counts": employee_counts,

        "total_departments": Department.objects.count(),
        "total_teams": Team.objects.count(),
        "total_team_members": TeamMember.objects.count(),
        "total_dependencies": Dependency.objects.count(),
        "total_meetings": Meeting.objects.count(),

        "recent_teams": recent_teams,
        "time_script": time_script,
        "time_div": time_div,
    }

    return render(request, "visualisation/visualisation_page.html", context)