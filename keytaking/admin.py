from django.contrib import admin
from keytaking.models import History, SettingsKeyTaking


@admin.register(History)
class PersonAdmin(admin.ModelAdmin):
    list_display = ("room", "fullname", "status", "is_return", "date")
    search_fields = ("room__startswith",)


@admin.register(SettingsKeyTaking)
class PersonAdmin(admin.ModelAdmin):
    list_display = ("confirmation_code", "code_timestamp", "is_confirm")

