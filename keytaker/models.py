import datetime
from django.db import models
from user.models import *

Floors = [
    ('1', '1'),
    ('2', '2'),
    ('3', '3')
]


class Room(models.Model):
    name = models.CharField(max_length=45)
    description = models.CharField(max_length=50, default="", blank=True, null=True)
    floor = models.CharField(max_length=2, choices=Floors, default='1')
    role = models.ManyToManyField(Role)
    is_occupied = models.BooleanField(default=False)
    is_visible = models.BooleanField(default=True)
    date = models.DateTimeField(blank=True, null=True)
    map_id = models.CharField(max_length=45,  blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Room'
        verbose_name_plural = 'Rooms'


class History(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, blank=True, null=True)
    fullname = models.CharField(max_length=50)
    role = models.ForeignKey(Role, on_delete=models.CASCADE, blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    is_return = models.BooleanField(default=False)
    user = models.ForeignKey(MainUser, on_delete=models.CASCADE, blank=True, null=True)
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


class SettingsKeyTaker(models.Model):
    confirmation_code = models.CharField(max_length=100)
    code_timestamp = models.DateTimeField(blank=True, null=True)
    is_confirm = models.BooleanField(default=False)
    in_process = models.BooleanField(default=False)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, blank=True, null=True)
    type = models.CharField(default='Manually', max_length=10, choices=TypeTakeRoom)
    step = models.IntegerField(default=1)
    error = models.CharField(max_length=100, default='', blank=True, null=True)

    def __str__(self):
        return self.confirmation_code

    class Meta:
        verbose_name = 'Settings KeyTaker'
        verbose_name_plural = 'Settings KeyTaker'


class Orders(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    confirmation_code = models.CharField(max_length=100)
    note = models.CharField(max_length=100, default='', blank=True, null=True)
    user = models.ForeignKey(MainUser, on_delete=models.CASCADE)
    orders_timestamp = models.DateTimeField()
    is_available = models.BooleanField(default=True)
    is_confirm = models.BooleanField(default=False)

    def __str__(self):
        return self.confirmation_code

    class Meta:
        verbose_name = 'Orders'
        verbose_name_plural = 'Orders'

