from colorfield.fields import ColorField
from random import randint

from django.db import models
from django.contrib.auth.models import User
from django.core import validators


class University(models.TextChoices):
    SNS = 'n', 'SNS'
    SSSUP = 's', 'SSSUP'


class RoomType(models.TextChoices):
    ROOM = 'c', 'Camera'
    STAIRS = 's', 'Scale'
    LIFT = 'a', 'Ascensore'


class Player(models.Model):
    user = models.OneToOneField(User, on_delete = models.PROTECT)

    def random_color():
        ran_hex = lambda : f'{randint(0, 255):x}'.zfill(2)
        return f'#{ran_hex()}{ran_hex()}{ran_hex()}'

    color = ColorField(default = random_color)

    university = models.CharField(max_length = 1, choices = University.choices, default = 'n')
    telegram_handle = models.CharField(max_length = 50, blank = True)
    eliminated = models.BooleanField(default = False)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'


class Room(models.Model):
    type = models.CharField(max_length = 1, choices = RoomType.choices, default = RoomType.ROOM)
    label = models.CharField(max_length = 20)
    tooltip = models.CharField(max_length = 30)
    floor = models.SmallIntegerField(validators = [
        validators.MinValueValidator(-1),
        validators.MaxValueValidator(+3),
    ], default = 0)
    svg_id = models.SmallIntegerField(default = 0)

    owner = models.ForeignKey(Player, related_name = 'room', on_delete = models.PROTECT, null = True)
    current_owner = models.ForeignKey(Player, related_name = 'current_rooms', on_delete = models.PROTECT, null = True)

    def __str__(self):
        return self.tooltip


class RoomConnection(models.Model):
    room1 = models.ForeignKey(Room, related_name = 'neighbours', on_delete = models.PROTECT)
    room1 = models.ForeignKey(Room, related_name = '+', on_delete = models.PROTECT)

    def __str__(self):
        return f'{str(self.room1)} -> {str(self.room2)}'


class Event(models.Model):
    attacker = models.ForeignKey(Player, related_name = '+', on_delete = models.PROTECT)
    attacker_room = models.ForeignKey(Room, related_name = '+', on_delete = models.PROTECT)
    target = models.ForeignKey(Player, related_name = '+', on_delete = models.PROTECT)
    target_room = models.ForeignKey(Room, related_name = '+', on_delete = models.PROTECT)

    time = models.DateTimeField(auto_now_add = True)
    announced = models.BooleanField(default = False)

    # add message text
