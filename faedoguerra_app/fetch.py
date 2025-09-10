from django.db.models import Count

from faedoguerra_app.models import Player, Room


def get_floor_map(floor):
    queryset = Room.objects.filter(floor = floor)

    def to_representation(instance):
        color = (255, 255, 255)

        if instance.current_owner != None:
            color = tuple(bytes.fromhex(instance.current_owner.color[1:]))

        return {
            'id': instance.id,
            'floor': floor,
            'svg_id': instance.svg_id,
            'color': color,
            'label': instance.label,
            'tooltip': instance.tooltip,
        }

    return list(map(to_representation, queryset))


def get_all_floors_maps():
    ret = []
    for floor in range(-1, 4):
        ret.extend(get_floor_map(floor))

    return ret


def get_ranking(count = 20):
    queryset = Player.objects\
        .annotate(room_count = Count('current_rooms'))\
        .order_by('room_count', 'id')\
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


def get_player(instance):
    rooms_queryset = Room.objects.filter(current_owner = instance)

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
    }


def get_room(instance):

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
    }

