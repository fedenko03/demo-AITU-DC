from django.contrib import admin
from .models import *


@admin.register(History)
class PersonAdmin(admin.ModelAdmin):
    list_display = ("room", "user", "fullname", "role", "is_verified", "is_return", "date")
    search_fields = ("fullname__startswith",)


@admin.register(SettingsKeyTaking)
class PersonAdmin(admin.ModelAdmin):
    list_display = ("confirmation_code", "code_timestamp", "is_confirm")


@admin.register(Room)
class PersonAdmin(admin.ModelAdmin):
    list_display = ("name", "floor", "is_occupied", "is_visible", "date")
    filter_horizontal = ("category",)
