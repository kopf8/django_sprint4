from django.shortcuts import render
from django.views.generic import TemplateView


class About(TemplateView):
    """CBV that displays "About" page based on 'about.html' template."""

    template_name = 'pages/about.html'


class Rules(TemplateView):
    """CBV that displays "Rules" page based on 'rules.html' template."""

    template_name = 'pages/rules.html'


def csrf_failure(request, reason=''):
    return render(request, 'pages/403csrf.html', status=403)


def page_not_found(request, exception):
    return render(request, 'pages/404.html', status=404)


def server_error(request):
    return render(request, 'pages/500.html', status=500)
