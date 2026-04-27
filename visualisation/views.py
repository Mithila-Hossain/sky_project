from django.shortcuts import render
from bokeh.plotting import figure
from bokeh.embed import components

def visualisation_home(request):

    # main line chart
    main_chart = figure(
    title="Project Activity Over Time",
    x_axis_label="Week",
    y_axis_label="Activity",
    height=280,
    sizing_mode="stretch_width"
)

    weeks = [1, 2, 3, 4, 5]
    activity = [10, 15, 20, 18, 25]

    main_chart.line(weeks, activity, line_width=3)
    main_chart.circle(weeks, activity, size=8)

    # category bar chart
    category_chart = figure(
    title="Category Breakdown",
    x_range=["Reports", "Messages", "Schedule", "Teams"],
    height=280,
    sizing_mode="stretch_width"
)

    categories = ["Reports", "Messages", "Schedule", "Teams"]
    values = [24, 138, 12, 8]

    category_chart.vbar(x=categories, top=values, width=0.6)

    # convert to HTML components
    main_script, main_div = components(main_chart)
    category_script, category_div = components(category_chart)

    return render(request, "visualisation/visualisation_page.html", {
        "main_script": main_script,
        "main_div": main_div,
        "category_script": category_script,
        "category_div": category_div,
    })