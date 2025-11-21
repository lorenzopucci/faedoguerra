from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.cache import cache_page
from django.views.decorators.clickjacking import xframe_options_exempt

from faedoguerra import settings
from faedoguerra_app import fetch
from faedoguerra_app.models import Player, Room


def home(request):
    return redirect('/dashboard')


@cache_page(settings.CACHE_TIMEOUT)
@xframe_options_exempt
def dashboard(request):
    return render(request, 'dashboard.jinja', {
        'svg_data': fetch.get_all_floors_maps(),
        'ranking': fetch.get_ranking(),
        'university_stats': fetch.get_university_stats(),
        'events': fetch.get_events(),
        'events_count': fetch.get_events_count(),
        'floor_to_focus': fetch.get_floor_to_focus(),
    })


@cache_page(settings.CACHE_TIMEOUT)
def ranking(request):
    return render(request, 'ranking.jinja', {
        'ranking': fetch.get_ranking(200, eliminated = True),
    })


@cache_page(settings.CACHE_TIMEOUT)
def events(request):
    return render(request, 'events.jinja', {
        'events': fetch.get_events(1000),
    })


@cache_page(settings.CACHE_TIMEOUT)
def about(request):
    return render(request, 'about.jinja')


@cache_page(settings.CACHE_TIMEOUT)
def privacy_policy(request):
    return render(request, 'privacy_policy.jinja')


@cache_page(settings.CACHE_TIMEOUT)
def player(request, player_id):
    instance = get_object_or_404(Player, id = player_id)
    return render(request, 'player.jinja', {
        'data': fetch.get_player(instance),
    })


@cache_page(settings.CACHE_TIMEOUT)
def room(request, room_id):
    instance = get_object_or_404(Room, id = room_id)
    return render(request, 'room.jinja', {
        'data': fetch.get_room(instance),
    })


@login_required
def user(request):
    return render(request, 'user.jinja')


@cache_page(settings.CACHE_TIMEOUT)
def replay_data(request):
    return JsonResponse(fetch.get_replay_data())
