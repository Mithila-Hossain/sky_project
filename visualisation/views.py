
# Author: Shayon Vincent | ID: w2090829

from django.shortcuts import render
from django.db.models import Count
from django.db.models.functions import TruncDate

from bokeh.plotting import figure
from bokeh.embed import components

from organisation.models import Department
from teams.models import Team, TeamMember, Dependency, Meeting


def visualisation_home(request):
    teams_queryset = Team.objects.all()

    # first chart: teams per department (bokeh)
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

    # second chart: team size distribution (bokeh)

    team_data = (
        Team.objects
            .annotate(member_count=Count("members"))
            .order_by("-member_count")
        )

    teams_with_members = [team for team in team_data if team.member_count > 0]
    empty_teams = [team for team in team_data if team.member_count == 0]

    selected_teams = teams_with_members[:8] + empty_teams[:2]

    team_names = [
        f"{team.name} (0)" if team.member_count == 0 else team.name
        for team in selected_teams
    ]


    member_counts = [team.member_count for team in selected_teams]

    if not team_names:
        team_names = ["No data"]
        member_counts = [0]

    colors = [
        "#d3d3d3" if count == 0 else "#0078D4"
        for count in member_counts

    ]

    category_chart = figure(
        title="Team Size (Members per Team)",
        y_range=team_names,   # ⭐ changed from x_range
        x_axis_label="Number of Members",
        y_axis_label="Team",
        height=350,
        sizing_mode="stretch_width",
        toolbar_location=None
    )

    category_chart.hbar(   # ⭐ changed from vbar
        y=team_names,
        right=member_counts,
        height=0.6,
        color=colors
    )

    category_chart.yaxis.major_label_text_font_size = "10pt"

    # third chart: employee count per department (chart.js)
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

    # fourth chart: teams created over time (bokeh)
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

    time_chart.line(
        x=created_dates,
        y=created_counts,
        line_width=3
    )

    time_chart.circle(
        x=created_dates,
        y=created_counts,
        size=8
    )

    time_chart.xaxis.major_label_orientation = 0.8

    # recent teams data
    recent_teams = (
        teams_queryset
        .select_related("department", "team_leader", "project")
        .order_by("-created_at")[:5]
    )

    # bokeh components
    main_script, main_div = components(main_chart)
    category_script, category_div = components(category_chart)
    time_script, time_div = components(time_chart)

    # context
    
    context = {
        "main_script": main_script,
        "main_div": main_div,

        "category_script": category_script,
        "category_div": category_div,

        "time_script": time_script,
        "time_div": time_div,

        "department_labels": department_labels,
        "employee_counts": employee_counts,

        "total_departments": Department.objects.count(),
        "total_teams": Team.objects.count(),
        "total_team_members": TeamMember.objects.count(),
        "total_dependencies": Dependency.objects.count(),
        "total_meetings": Meeting.objects.count(),

        "recent_teams": recent_teams,
    }

    return render(request, "visualisation/visualisation_page.html", context)