from django.contrib import admin

from main.models import PIN


@admin.register(PIN)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("code", "is_locked")
