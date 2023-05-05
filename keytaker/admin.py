from django.contrib import admin
from .models import *


@admin.register(History)
class PersonAdmin(admin.ModelAdmin):
    list_display = ("room", "user", "fullname", "role", "is_verified", "is_return", "date")
    search_fields = ("fullname__startswith",)


@admin.register(SettingsKeyTaker)
class PersonAdmin(admin.ModelAdmin):
    list_display = ("confirmation_code", "code_timestamp", "is_confirm")


@admin.register(Room)
class PersonAdmin(admin.ModelAdmin):
    list_display = ("name", "floor", "is_occupied", "is_visible", "date")
    filter_horizontal = ("role",)
    search_fields = ("name__startswith",)
    actions = ['make_occupied']

    def make_occupied(self, request, queryset):
        for room in queryset:
            room.is_occupied = not room.is_occupied
            room.save()

    make_occupied.short_description = "Toggle occupancy for selected rooms"


@admin.register(Orders)
class PersonAdmin(admin.ModelAdmin):
    list_display = ("room", "confirmation_code", "user", "is_available", "is_confirm")


@admin.register(Reservation)
class PersonAdmin(admin.ModelAdmin):
    list_display = ("room", "key", "start_time", "is_take", "is_active")


@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ("day", "room", "start_time_formatted", "end_time_formatted", "professor")

    def start_time_formatted(self, obj):
        return obj.start_time.strftime('%H:%M')

    def end_time_formatted(self, obj):
        return obj.end_time.strftime('%H:%M')

    start_time_formatted.short_description = "Start Time"
    end_time_formatted.short_description = "End Time"

    search_fields = ("room__name", "professor__full_name")
    list_filter = ("day", "room__floor", "professor__role", "room__name")


@admin.register(StudyRoomSchedule)
class StudyRoomScheduleAdmin(admin.ModelAdmin):
    list_display = ("room", "start_time_formatted", "end_time_formatted", "professor", "status")

    def start_time_formatted(self, obj):
        return obj.start_time.strftime('%H:%M')

    def end_time_formatted(self, obj):
        return obj.end_time.strftime('%H:%M')

    start_time_formatted.short_description = "Start Time"
    end_time_formatted.short_description = "End Time"

    search_fields = ("room__name", "professor__full_name")
    list_filter = ("room__floor", "professor__role", "status", "room__name")
