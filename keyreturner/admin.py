from django.contrib import admin

from keyreturner.models import SettingsKeyReturner


@admin.register(SettingsKeyReturner)
class PersonAdmin(admin.ModelAdmin):
    list_display = ("token", "token_timestamp", "in_process", "user", "step", "error")
    search_fields = ("token__startswith",)
