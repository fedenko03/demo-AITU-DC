from django.db import models


class History(models.Model):
    room = models.CharField(max_length=25),
    fullname = models.CharField(max_length=50),
    status = models.CharField(max_length=10)
