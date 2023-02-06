from django.contrib.auth.models import User
from django.db import models


class CustomUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    confirmation_code = models.CharField(max_length=32, blank=True, null=True)
    code_timestamp = models.DateTimeField(blank=True, null=True)
    auth_token = models.CharField(max_length=100)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
