from colorfield.fields import ColorField
from random import randint

from django.db import models
from django.contrib.auth.models import User
from django.core import validators
from django.utils import timezone


class University(models.TextChoices):
    SNS = 'n', 'SNS'
    SSSUP = 's', 'SSSUP'
    OTHER = 'e', 'Esterno'


class AnnouncementType(models.TextChoices):
    ATTACK = 'a', 'Attacco con difensore'
    ATTACK_NO_DEFENDER = 'n', 'Attacco senza difensore'
    ATTACK_ELIMINATION = 'e', 'Attacco con eliminazione'
    OTHER = 'o', 'Altro'


class Player(models.Model):
    user = models.OneToOneField(User, on_delete = models.PROTECT)

    def random_color():
        ran_hex = lambda : f'{randint(0, 255):x}'.zfill(2)
        return f'#{ran_hex()}{ran_hex()}{ran_hex()}'

    color = ColorField(default = random_color)

    university = models.CharField(max_length = 1, choices = University.choices, default = 'n')

    telegram_handle = models.CharField(max_length = 50, blank = True)
    telegram_chat_id = models.IntegerField(default = 0)

    eliminated = models.BooleanField(default = False)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'


class Room(models.Model):
    label = models.CharField(max_length = 20)
    tooltip = models.CharField(max_length = 30)
    floor = models.SmallIntegerField(validators = [
        validators.MinValueValidator(-1),
        validators.MaxValueValidator(+3),
    ], default = 0)
    svg_id = models.SmallIntegerField(default = 0)

    owner = models.ForeignKey(Player, related_name = 'room', on_delete = models.PROTECT, blank = True, null = True)
    current_owner = models.ForeignKey(Player, related_name = 'current_rooms', on_delete = models.PROTECT, blank = True, null = True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields = ['floor', 'svg_id'], name = 'unique_svg_path'
            )
        ]

    def __str__(self):
        return self.tooltip


class Announcement(models.Model):
    type = models.CharField(max_length = 1, choices = AnnouncementType.choices)
    string = models.CharField(max_length = 300)

    def __str__(self):
        return self.string


class Event(models.Model):
    attacker = models.ForeignKey(Player, related_name = '+', on_delete = models.PROTECT)
    attacker_room = models.ForeignKey(Room, related_name = '+', on_delete = models.PROTECT, blank = True, null = True)

    target = models.ForeignKey(Player, related_name = '+', on_delete = models.PROTECT, blank = True, null = True)
    target_room = models.ForeignKey(Room, related_name = '+', on_delete = models.PROTECT)

    time = models.DateTimeField(blank = True)
    announced = models.BooleanField(default = False)
    announcement = models.ForeignKey(Announcement, on_delete = models.PROTECT, null = True)

    def save(self, *args, **kwargs):
        if not self.id:
            self.time = timezone.now()
        return super(Event, self).save(*args, **kwargs)

    @property
    def filled_announcement(self):
        return self.announcement.string.format(
            attacker = str(self.attacker),
            attacker_room = str(self.attacker_room),
            target = str(self.target),
            target_room = str(self.target_room),
        )

    def __str__(self):
        marker = "[*] " if not self.announced else ""
        return f"{marker}{self.time.strftime('%d/%m/%Y, %H:%M')} {self.attacker} -> {self.target_room}"
