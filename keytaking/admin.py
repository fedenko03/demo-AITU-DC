from django.contrib import admin
from keytaking.models import History


@admin.register(History)
class PersonAdmin(admin.ModelAdmin):
    list_display = ("room", "fullname", "status", "is_return", "date")
    search_fields = ("room__startswith",)

