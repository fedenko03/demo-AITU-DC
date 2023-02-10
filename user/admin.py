from django.contrib import admin
from .models import *


@admin.register(MainUser)
class PersonAdmin(admin.ModelAdmin):
    list_display = ("full_name", "email", "role", "is_active", "confirmation_code")
    search_fields = ("full_name__startswith",)


@admin.register(Role)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)

