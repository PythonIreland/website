from django.contrib import admin
from meetups.models import Meetup, MeetupSponsorRelationship

class MeetupSponsorRelationshipInline(admin.TabularInline):
    model = MeetupSponsorRelationship
    extra = 1

@admin.register(Meetup)
class MeetupAdmin(admin.ModelAdmin):
    inlines = [
        MeetupSponsorRelationshipInline
    ]

@admin.register(MeetupSponsorRelationship)
class MeetupSponsorRelationshipAdmin(admin.ModelAdmin):
    list_display = ('meetup', 'sponsor')
    list_editable = ('meetup', 'sponsor')
    list_filter = ('sponsor',)
