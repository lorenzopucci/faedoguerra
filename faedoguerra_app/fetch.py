import math

from django.db.models import Count, Q
from django.utils import timezone

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

        ret = {
            'id': instance.id,
            'floor': floor,
            'svg_id': instance.svg_id,
            'color': color,
            'label': instance.label,
            'tooltip': instance.tooltip,
        }
        if len(events) > 0 and events[0].target_room == instance:
            ret['blink'] = True

        return ret

    return list(map(to_representation, queryset))


def get_all_floors_maps():
    ret = []
    for floor in range(-1, 4):
        ret.extend(get_floor_map(floor))

    return ret


def get_ranking(count = 15, eliminated = False):
    queryset = Player.objects.all()

    if not eliminated:
        queryset = queryset.exclude(eliminated = True)

    queryset = queryset\
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


def to_university_percentages(sns_count, sssup_count):
    def round_down(x):
        return str(math.floor(10 * x) / 10)

    return {
        'sns': round_down(100 * sns_count / (sns_count + sssup_count)),
        'sssup': round_down(100 * sssup_count / (sns_count + sssup_count)),
    }


def get_university_stats():
    sns_count = Room.objects\
        .filter(current_owner__university = 'n')\
        .count()

    sssup_count = Room.objects\
        .filter(current_owner__university = 's')\
        .count()

    def round_down(x):
        return str(math.floor(10 * x) / 10)

    return to_university_percentages(sns_count, sssup_count)


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
    current_tz = timezone.get_current_timezone()

    def to_representation(event):
        return {
            'time': event.time.astimezone(current_tz).strftime('%d/%m/%Y, %H:%M'),
            'announcement': to_event_html_string(event)
        }

    return list(map(to_representation, queryset))


def get_events(count = 10):
    queryset = Event.objects\
        .all()\
        .order_by('-time')\
        [:count]

    return get_events_from_queryset(queryset)


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


def get_events_count():
    return Event.objects.exclude(announcement__type = 'o').count()


def get_replay_data(ranking_count = 15):
    events = Event.objects\
        .exclude(announcement__type = 'o')\
        .order_by('time')


    # details of the single update to apply to the map at each transition
    def to_delta_representation(instance):
        target_color = (255, 255, 255)

        if instance.target is not None:
            target_color = color_hex_to_tuple(instance.target.color)

        return {
            'floor': instance.target_room.floor,
            'svg_id': instance.target_room.svg_id,
            'new_color': color_hex_to_tuple(instance.attacker.color),
            'old_color': target_color,
        }


    # annotate initial room count
    players = Player.objects.all().annotate(room_count = Count('room'))

    # {<player_instance>: <room_count>} to keep track of room counts
    rooms_count = dict(zip(
        players,
        players.values_list('room_count', flat = True),
    ))

    sns_count = Room.objects.filter(owner__university = 'n').count()
    sssup_count = Room.objects.filter(owner__university = 's').count()


    def to_ranking_item(item_data):
        instance, count = item_data

        return {
            'id': instance.id,
            'full_name': str(instance),
            'university': instance.get_university_display(),
            'color': instance.color,
            'count': count,
        }

    def generate_ranking():
        sorted_data = sorted(rooms_count.items(), key = lambda x: (-x[1], x[0].id))
        return list(map(to_ranking_item, sorted_data[:ranking_count]))


    # rankings at all timespamps
    ranking = [generate_ranking()]

    #university stats at all timestamps
    university_stats = [to_university_percentages(sns_count, sssup_count)]

    for event in events:
        rooms_count[event.attacker] += 1

        if event.attacker.university == 'n':
            sns_count += 1
        else:
            sssup_count += 1

        if event.announcement.type == 'a':
            rooms_count[event.target] -= 1

        elif event.announcement.type == 'e':
            del rooms_count[event.target]

        if event.announcement.type in ['a', 'e']:
            if event.target.university == 'n':
                sns_count -= 1
            else:
                sssup_count -= 1

        ranking.append(generate_ranking())
        university_stats.append(to_university_percentages(sns_count, sssup_count))


    return {
        'ranking': ranking,
        'university_stats': university_stats,
        'deltas': list(map(to_delta_representation, events)),
    }
