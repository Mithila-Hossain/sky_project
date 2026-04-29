from django.shortcuts import render


def report_home_view(request):

    context = {
        'title': 'Sky Project Analytics',
        'description': 'This is the official team registry report page.'
    }
    return render(request, 'reports/report_page.html', context)