from django.db import models

from user.models import MainUser


class SettingsKeyReturner(models.Model):
    token = models.CharField(max_length=100)
    token_timestamp = models.DateTimeField(blank=True, null=True)
    in_process = models.BooleanField(default=False)
    user = models.ForeignKey(MainUser, on_delete=models.CASCADE, blank=True, null=True)
    step = models.IntegerField(default=1)
    error = models.CharField(max_length=100, default='', blank=True, null=True)

    def __str__(self):
        return self.token

    class Meta:
        verbose_name = 'Settings KeyReturner'
        verbose_name_plural = 'Settings KeyReturner'
