import datetime
from django.db import models
from user.models import *


class History(models.Model):
    room = models.CharField(max_length=25)
    fullname = models.CharField(max_length=50)
    status = models.CharField(max_length=10, default=False)
    is_return = models.BooleanField(default=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True)
    date = models.DateTimeField(max_length=10, auto_now_add=True)

    def __str__(self):
        return self.room

    class Meta:
        verbose_name = 'History'
        verbose_name_plural = 'History'


class SettingsKeyTaking(models.Model):
    confirmation_code = models.CharField(max_length=100)
    code_timestamp = models.DateTimeField(blank=True, null=True)
    is_confirm = models.BooleanField(default=False)
    room = models.CharField(max_length=20, default="")

    class Meta:
        verbose_name = 'Settings KeyTaking'
        verbose_name_plural = 'Settings KeyTaking'
