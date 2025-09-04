from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required


def home(request):
    return redirect('/dashboard')


def dashboard(request):
    return render(request, 'dashboard.jinja')


def about(request):
    return render(request, 'about.jinja')


@login_required
def user(request):
    return render(request, 'user.jinja')
