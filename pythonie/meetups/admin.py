from django.contrib import admin
from meetups.models import Meetup, MeetupUpdate, MeetupSponsorRelationship

class MeetupSponsorRelationshipInline(admin.TabularInline):
    model = MeetupSponsorRelationship
    extra = 1

class MeetupAdmin(admin.ModelAdmin):
    inlines = [
        MeetupSponsorRelationshipInline
    ]

admin.site.register(Meetup, MeetupAdmin)
admin.site.register(MeetupSponsorRelationship)
admin.site.register(MeetupUpdate)
