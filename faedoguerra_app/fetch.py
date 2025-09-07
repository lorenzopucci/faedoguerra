from faedoguerra_app.models import Room


def get_floor_map(floor):
    queryset = Room.objects.filter(floor = floor)

    def to_representation(instance):
        color = (255, 255, 255)

        if instance.current_owner != None:
            color = tuple(bytes.fromhex(instance.current_owner.color[1:]))

        return {
            "id": instance.id,
            "floor": floor,
            "svg_id": instance.svg_id,
            "color": color,
            "label": instance.label,
            "tooltip": instance.tooltip,
        }

    return list(map(to_representation, queryset))


def get_all_floors_maps():
    ret = []
    for floor in range(-1, 4):
        ret.extend(get_floor_map(floor))

    return ret
