from django.contrib import admin
from .models import CustomUser


@admin.register(CustomUser)
class PersonAdmin(admin.ModelAdmin):
    list_display = ("full_name", "email", "role", "is_active", "confirmation_code")
    search_fields = ("full_name__startswith",)

