from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import Http404

from faedoguerra_app import fetch


def home(request):
    return redirect('/dashboard')


def dashboard(request):
    return render(request, 'dashboard.jinja', {
        'floor': '',
        'data': fetch.get_all_floors_maps(),
        'ranking': fetch.get_ranking(),
    })


def dashboard_floor(request, floor):
    if not floor in ["-1", "0", "1", "2", "3"]:
        raise Http404("Piano inesistente")
    else:
        return render(request, 'dashboard.jinja', {
            'floor': floor,
            'data': fetch.get_floor_map(int(floor)),
            'ranking': fetch.get_ranking(),
        })


def about(request):
    return render(request, 'about.jinja')


@login_required
def user(request):
    return render(request, 'user.jinja')
