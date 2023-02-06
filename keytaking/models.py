import datetime
from django.db import models
from user.models import *


UserRole = [
    ('Student', 'Student'),
    ('Professor', 'Professor'),
    ('Other', 'Other')
]


RoomCategory = [
    ('Staff only', 'Staff only'),
    ('For everyone', 'For everyone')
]


class Room(models.Model):
    name = models.CharField(max_length=15)
    category = models.CharField(max_length=15, choices=RoomCategory)
    is_occupied = models.BooleanField(default=False)
    is_visible = models.BooleanField(default=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True)
    date = models.DateTimeField(blank=True, null=True)

    class Meta:
        verbose_name = 'Room'
        verbose_name_plural = 'Rooms'


class History(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, blank=True, null=True)
    fullname = models.CharField(max_length=50)
    role = models.CharField(max_length=32, choices=UserRole)
    is_verified = models.BooleanField(default=False)
    is_return = models.BooleanField(default=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True)
    date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.room

    class Meta:
        verbose_name = 'History'
        verbose_name_plural = 'History'


class SettingsKeyTaking(models.Model):
    confirmation_code = models.CharField(max_length=100)
    code_timestamp = models.DateTimeField(blank=True, null=True)
    is_confirm = models.BooleanField(default=False)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.confirmation_code

    class Meta:
        verbose_name = 'Settings KeyTaking'
        verbose_name_plural = 'Settings KeyTaking'
