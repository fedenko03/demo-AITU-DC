import datetime
from django.db import models


class History(models.Model):
    room = models.CharField(max_length=25)
    fullname = models.CharField(max_length=50)
    status = models.CharField(max_length=10)
    is_return = models.BooleanField(default=False)
    date = models.DateTimeField(max_length=10, auto_now_add=True)

    def __str__(self):
        return self.room

    class Meta:
        verbose_name = 'History'
        verbose_name_plural = 'History'
