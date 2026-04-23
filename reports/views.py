from django.shortcuts import render
# If you want to show teams later, we will import the Team model here

def report_home_view(request):
    # For now, let's just send a simple title to the page
    context = {
        'title': 'Sky Project Analytics',
        'description': 'This is the official team registry report page.'
    }
    return render(request, 'reports/report_page.html', context)