from django.db import models


class PIN(models.Model):
    code = models.CharField(max_length=15, default='')
    is_locked = models.BooleanField(default=False)

    def __str__(self):
        return self.code

    class Meta:
        verbose_name = 'PIN code'
        verbose_name_plural = 'PIN code'
