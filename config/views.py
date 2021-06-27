from django.shortcuts import render

ABOUT_TEXT = (
    'Я - Дмитрий, только учусь программированию на Python, не судите строго')
TECHNOLOGY_TEXT = (
    'В этом проекте использовались технологии: Django, DRF, Python, JS'
)


def server_error(request):
    return render(
        request,
        'misc/500.html',
        status=500
    )


def page_not_found(request, exception):
    return render(
        request,
        'misc/404.html',
        {'path': request.path},
        status=404
    )


def author(request):
    return render(
        request,
        'flatpages/about.html',
        {'text': ABOUT_TEXT,
         'title': 'Об авторе'},
        status=200
    )


def technology(request):
    return render(
        request,
        'flatpages/about.html',
        {'text': TECHNOLOGY_TEXT,
         'title': 'Об авторе'},
        status=200
    )

