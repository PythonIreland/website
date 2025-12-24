from django.contrib import admin

from speakers.models import Room, Session, Speaker


class RoomAdmin(admin.ModelAdmin):
    list_display = ("name",)


admin.site.register(Room, RoomAdmin)


class SpeakerAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "email",
    )


admin.site.register(Speaker, SpeakerAdmin)


class SessionAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "speaker_names",
        "room",
        "type",
        "state",
        "scheduled_at",
    )

    list_filter = ("room", "state", "type")

    search_fields = ["name", "room", "type", "state"]

    @admin.display()
    def speaker_names(self, obj):
        return ", ".join(speaker.name for speaker in obj.speakers.all())


admin.site.register(Session, SessionAdmin)
