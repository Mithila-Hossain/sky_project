from django.shortcuts import render
from django.db.models import Count

from bokeh.plotting import figure
from bokeh.embed import components

from organisation.models import Department
from teams.models import Team, TeamMember, Dependency, Meeting


def visualisation_home(request):

    # =========================
    # CHART 1: Department vs Teams
    # =========================
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

    # =========================
    # CHART 2: Team Status Breakdown
    # =========================
    status_data = (
        Team.objects
        .values("status")
        .annotate(status_count=Count("id"))
        .order_by("status")
    )

    statuses = [item["status"] or "Unknown" for item in status_data]
    status_counts = [item["status_count"] for item in status_data]

    if not statuses:
        statuses = ["No data"]
        status_counts = [0]

    category_chart = figure(
        title="Team Status Breakdown",
        x_range=statuses,
        x_axis_label="Team Status",
        y_axis_label="Number of Teams",
        height=350,
        sizing_mode="stretch_width",
        toolbar_location=None
    )

    category_chart.vbar(
        x=statuses,
        top=status_counts,
        width=0.6
    )

    category_chart.xaxis.major_label_orientation = 0.8

    # =========================
    # CHART 3: Employees by Department for Chart.js
    # =========================
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

    # =========================
    # Bokeh Components
    # =========================
    main_script, main_div = components(main_chart)
    category_script, category_div = components(category_chart)

    # =========================
    # Context
    # =========================
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
    }

    return render(request, "visualisation/visualisation_page.html", context)