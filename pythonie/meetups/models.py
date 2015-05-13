from django.db import models

import logging

log = logging.getLogger('meetups')


class MeetupUpdate(models.Model):
    updated = models.DateTimeField(auto_now=True)


class Meetup(models.Model):
    id = models.CharField(max_length=100, primary_key=True)

    name = models.CharField(max_length=255, blank=False)
    description = models.TextField()
    announced = models.BooleanField(default=False)
    meetup_url = models.URLField()

    time = models.DateTimeField()
    created = models.DateTimeField()
    updated = models.DateTimeField()

    rsvps = models.IntegerField(default=0)
