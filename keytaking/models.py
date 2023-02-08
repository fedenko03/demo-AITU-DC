import datetime
from django.db import models
from user.models import *

Floors = [
    ('1', '1'),
    ('2', '2'),
    ('3', '3')
]


class Room(models.Model):
    name = models.CharField(max_length=15)
    floor = models.CharField(max_length=2, choices=Floors, default='1')
    category = models.ManyToManyField(Category)
    is_occupied = models.BooleanField(default=False)
    is_visible = models.BooleanField(default=True)
    date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Room'
        verbose_name_plural = 'Rooms'


class History(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, blank=True, null=True)
    fullname = models.CharField(max_length=50)
    role = models.ForeignKey(Category, on_delete=models.CASCADE)
    is_verified = models.BooleanField(default=False)
    is_return = models.BooleanField(default=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True)
    date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.fullname

    class Meta:
        verbose_name = 'History'
        verbose_name_plural = 'History'


TypeTakeRoom = [
    ('QR', 'QR'),
    ('Manually', 'Manually')
]


class SettingsKeyTaking(models.Model):
    confirmation_code = models.CharField(max_length=100)
    code_timestamp = models.DateTimeField(blank=True, null=True)
    is_confirm = models.BooleanField(default=False)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, blank=True, null=True)
    type = models.CharField(default='Manually', max_length=10, choices=TypeTakeRoom)
    step = models.IntegerField(default=1)
    error = models.CharField(max_length=100, default='', blank=True, null=True)

    def __str__(self):
        return self.confirmation_code

    class Meta:
        verbose_name = 'Settings KeyTaking'
        verbose_name_plural = 'Settings KeyTaking'
