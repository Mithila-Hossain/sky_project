from django.shortcuts import render
from django.db.models import Count
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.models import ColumnDataSource, HoverTool

from organisation.models import Department
from teams.models import Team, TeamMember, Dependency, Meeting


def visualisation_home(request):
    # Chart 1: Department name vs number of teams/projects
    department_data = (
        Department.objects
        .annotate(team_count=Count("team"))
        .order_by("name")
    )

    department_names = [dept.name for dept in department_data]
    team_counts = [dept.team_count for dept in department_data]

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

    # Chart 2: Department head vs project/team names
    teams = Team.objects.select_related("department", "department__head", "project").all()

    team_names = []
    team_values = []
    department_heads = []
    departments = []

    for team in teams:
        team_names.append(team.name)
        team_values.append(1)
        departments.append(team.department.name if team.department else "No department")

        if team.department and team.department.head:
            department_heads.append(team.department.head.username)
        else:
            department_heads.append("No head assigned")

    if not team_names:
        team_names = ["No data"]
        team_values = [0]
        department_heads = ["No data"]
        departments = ["No data"]

    source = ColumnDataSource(data={
        "team_names": team_names,
        "team_values": team_values,
        "department_heads": department_heads,
        "departments": departments,
    })

    category_chart = figure(
        title="Department Head vs Team / Project Name",
        x_range=team_names,
        x_axis_label="Team / Project Name",
        y_axis_label="Count",
        height=350,
        sizing_mode="stretch_width",
        toolbar_location=None
    )

    category_chart.vbar(
        x="team_names",
        top="team_values",
        width=0.6,
        source=source
    )

    category_chart.add_tools(HoverTool(tooltips=[
        ("Team / Project", "@team_names"),
        ("Department", "@departments"),
        ("Department Head", "@department_heads"),
    ]))

    category_chart.xaxis.major_label_orientation = 0.8

    main_script, main_div = components(main_chart)
    category_script, category_div = components(category_chart)

    context = {
        "main_script": main_script,
        "main_div": main_div,
        "category_script": category_script,
        "category_div": category_div,

        "total_departments": Department.objects.count(),
        "total_teams": Team.objects.count(),
        "total_team_members": TeamMember.objects.count(),
        "total_dependencies": Dependency.objects.count(),
        "total_meetings": Meeting.objects.count(),
    }

    return render(request, "visualisation/visualisation_page.html", context)