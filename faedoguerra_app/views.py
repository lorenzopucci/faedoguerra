from django.shortcuts import render, redirect


def home(request):
    return redirect('/dashboard')


def dashboard(request):
    return render(request, 'dashboard.jinja')


def about(request):
    return render(request, 'about.jinja')

