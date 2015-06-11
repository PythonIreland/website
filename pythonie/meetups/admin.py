from django.contrib import admin
from meetups.models import Meetup, MeetupUpdate

admin.site.register(Meetup)
admin.site.register(MeetupUpdate)