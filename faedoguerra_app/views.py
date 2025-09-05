from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import Http404


def home(request):
    return redirect('/dashboard')


def dashboard(request):
    return render(request, 'dashboard.jinja', {'floor': ""})


def dashboard_floor(request, floor):
    if not floor in ["-1", "0", "1", "2", "3"]:
        raise Http404("Piano inesistente")
    else:
        return render(request, 'dashboard.jinja', {'floor': floor})


def about(request):
    return render(request, 'about.jinja')


@login_required
def user(request):
    return render(request, 'user.jinja')
