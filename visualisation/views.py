from django.shortcuts import render
from bokeh.plotting import figure
from bokeh.embed import components


def visualisation_home(request):
    # Main line chart
    main_chart = figure(
        title="Project Activity Over Time",
        x_axis_label="Week",
        y_axis_label="Activity Count",
        height=300,
        sizing_mode="stretch_width"
    )

    weeks = [1, 2, 3, 4, 5]
    activity = [10, 18, 14, 25, 30]

    main_chart.line(weeks, activity, line_width=3)
    main_chart.circle(weeks, activity, size=8)

    # Category breakdown bar chart
    category_chart = figure(
        title="Category Breakdown",
        x_range=["Reports", "Messages", "Schedule", "Teams"],
        y_axis_label="Count",
        height=300,
        sizing_mode="stretch_width"
    )

    categories = ["Reports", "Messages", "Schedule", "Teams"]
    counts = [24, 138, 12, 8]

    category_chart.vbar(x=categories, top=counts, width=0.6)

    # Convert Bokeh charts into script and divs
    main_script, main_div = components(main_chart)
    category_script, category_div = components(category_chart)

    context = {
        "main_script": main_script,
        "main_div": main_div,
        "category_script": category_script,
        "category_div": category_div,
    }

    return render(request, "visualisation/visualisation_page.html", context)