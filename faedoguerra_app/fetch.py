import math

from django.db.models import Count, Q

from faedoguerra_app.models import Player, Room, Event


def color_hex_to_tuple(color):
    return tuple(bytes.fromhex(color[1:]))


def get_floor_map(floor):
    queryset = Room.objects.filter(floor = floor)
    events = Event.objects\
        .exclude(announcement__type = 'o')\
        .order_by('-id')\
        [:1]

    def to_representation(instance):
        color = (255, 255, 255)

        if instance.current_owner != None:
            color = color_hex_to_tuple(instance.current_owner.color)

        return {
            'id': instance.id,
            'floor': floor,
            'svg_id': instance.svg_id,
            'color': color,
            'label': instance.label,
            'tooltip': instance.tooltip,
            'blink': len(events) > 0 and events[0].target_room == instance,
        }

    return list(map(to_representation, queryset))


def get_all_floors_maps():
    ret = []
    for floor in range(-1, 4):
        ret.extend(get_floor_map(floor))

    return ret


def get_ranking(count = 20):
    queryset = Player.objects\
        .filter(eliminated = False)\
        .annotate(room_count = Count('current_rooms'))\
        .order_by('-room_count', 'id')\
        [:count]

    def to_representation(arg):
        rank, instance = arg

        return {
            'rank': rank + 1,
            'id': instance.id,
            'full_name': str(instance),
            'room_count': instance.room_count,
            'university': instance.get_university_display(),
            'color': instance.color,
        }

    return list(map(to_representation, enumerate(queryset)))


def get_university_stats():
    sns_count = Room.objects\
        .filter(current_owner__university = 'n')\
        .count()

    sssup_count = Room.objects\
        .filter(current_owner__university = 's')\
        .count()

    def round_down(x):
        return str(math.floor(10 * x) / 10)

    return {
        'sns_count': sns_count,
        'sssup_count': sssup_count,
        'sns_percentage': round_down(100 * sns_count / (sns_count + sssup_count)),
        'sssup_percentage': round_down(100 * sssup_count / (sns_count + sssup_count)),
    }


def to_event_html_string(event):
    target = ''
    if event.target is not None:
        target = f'<a href="/player/{event.target.id}">{event.target}</a>'

    return event.announcement.string.format(
        attacker = f'<a href="/player/{event.attacker.id}">{event.attacker}</a>',
        attacker_room = f'<a href="/room/{event.attacker_room.id}">{event.attacker_room}</a>',
        target = target,
        target_room = f'<a href="/room/{event.target_room.id}">{event.target_room}</a>',
    )


def get_events_from_queryset(queryset):
    def to_representation(event):
        return {
            'time': event.time.strftime('%d/%m/%Y, %H:%M'),
            'announcement': to_event_html_string(event)
        }

    return list(map(to_representation, queryset))


def get_events(count = 20):
    queryset = Event.objects\
        .all()\
        .order_by('-time')\
        [:count]

    return get_events_from_queryset(queryset)


def get_replay_data():
    queryset = Event.objects\
        .exclude(announcement__type = 'o')\
        .order_by('time')

    def to_representation(instance):
        target_color = (255, 255, 255)

        if instance.target is not None:
            target_color = color_hex_to_tuple(instance.target.color)

        return {
            'floor': instance.target_room.floor,
            'svg_id': instance.target_room.svg_id,
            'new_color': color_hex_to_tuple(instance.attacker.color),
            'old_color': target_color,
        }

    return list(map(to_representation, queryset))


def get_player(instance):
    rooms_queryset = Room.objects.filter(current_owner = instance)

    events_queryset = Event.objects\
        .filter(Q(attacker = instance) | Q(target = instance))\
        .order_by('-time')


    def to_room_representation(room):
        return {
            'id': room.id,
            'tooltip': room.tooltip,
        }

    return {
        'full_name': str(instance),
        'university': instance.get_university_display(),
        'own_room': to_room_representation(instance.room.all()[0]),
        'rooms': list(map(to_room_representation, rooms_queryset)),
        'rooms_count': len(rooms_queryset),
        'events': get_events_from_queryset(events_queryset),
    }


def get_room(instance):
    events_queryset = Event.objects\
        .filter(target_room = instance)\
        .order_by('-time')

    def to_player_representation(data):
        if data == None:
            return False
        return {
            'id': data.id,
            'full_name': str(data),
            'university': data.get_university_display(),
        }

    return {
        'tooltip': instance.tooltip,
        'floor': instance.floor,
        'owner': to_player_representation(instance.owner),
        'current_owner': to_player_representation(instance.current_owner),
        'events': get_events_from_queryset(events_queryset),
    }

