from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import Http404

from faedoguerra_app import fetch
from faedoguerra_app.models import Player, Room


def home(request):
    return redirect('/dashboard')


def dashboard(request):
    return render(request, 'dashboard.jinja', {
        'floor': '',
        'data': fetch.get_all_floors_maps(),
        'ranking': fetch.get_ranking(),
        'university_stats': fetch.get_university_stats(),
        'events': fetch.get_events(),
    })


def dashboard_floor(request, floor):
    if not floor in ["-1", "0", "1", "2", "3"]:
        raise Http404("Piano inesistente")
    else:
        return render(request, 'dashboard.jinja', {
            'floor': floor,
            'data': fetch.get_floor_map(int(floor)),
            'ranking': fetch.get_ranking(),
            'university_stats': fetch.get_university_stats(),
            'events': fetch.get_events(),
        })


def about(request):
    return render(request, 'about.jinja')


def player(request, player_id):
    instance = get_object_or_404(Player, id = player_id)
    return render(request, 'player.jinja', {
        'data': fetch.get_player(instance),
    })


def room(request, room_id):
    instance = get_object_or_404(Room, id = room_id)
    return render(request, 'room.jinja', {
        'data': fetch.get_room(instance),
    })


@login_required
def user(request):
    return render(request, 'user.jinja')
