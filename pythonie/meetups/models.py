from datetime import datetime, timedelta
from django.db import models

import logging
from pytz import UTC

log = logging.getLogger('meetups')


class MeetupUpdate(models.Model):
    updated = models.DateTimeField(auto_now_add=True)

    @classmethod
    def tick(cls):
        meetup_update = cls.objects.filter().first()
        now = datetime.now(tz=UTC)
        if not meetup_update:
            meetup_update = cls()
        meetup_update.updated = now
        meetup_update.save()

    @classmethod
    def _invalidate_meetup_update(cls):
        # Invalidate the MeetupUpdate by making more than an hour ago
        meetup_update = cls.objects.filter().get()
        meetup_update.updated = datetime.now(tz=UTC) - timedelta(hours=1)
        meetup_update.save(force_update=True, update_fields=['updated'])


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
