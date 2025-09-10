from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from faedoguerra_app.models import Player, Room, RoomConnection, Event


class PlayerInline(admin.StackedInline):
    model = Player
    can_delete = False


class UserAdmin(BaseUserAdmin):
    inlines = [PlayerInline]


admin.site.unregister(User)
admin.site.register(User, UserAdmin)

admin.site.register(Room)
admin.site.register(RoomConnection)
admin.site.register(Event)
