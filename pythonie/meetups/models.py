from datetime import datetime, timedelta, date
from django.db import models

from sponsors.models import Sponsor
from wagtail.wagtailsnippets.models import register_snippet
from delorean import Delorean
from delorean.dates import UTC

import logging
log = logging.getLogger('meetups')


def next_n_months(source_date, months):
    month = source_date.month - 1 + months
    year = source_date.year + month // 12
    month = month % 12 + 2
    return date(year, month, 1)


class MeetupSponsorRelationship(models.Model):
    """ Qualify how sponsor helped what meetup
    Pivot table for Sponsor M<-->M Meetup
    """
    sponsor = models.ForeignKey(Sponsor)
    meetup = models.ForeignKey('Meetup')
    note = models.TextField(blank=True, default='')


@register_snippet
class Meetup(models.Model):
    id = models.CharField(max_length=100, primary_key=True)

    name = models.CharField(max_length=255, blank=False)
    description = models.TextField()
    event_url = models.URLField()

    sponsors = models.ManyToManyField(Sponsor, through=MeetupSponsorRelationship, null=True, blank=True)

    time = models.DateTimeField()
    created = models.DateTimeField()
    updated = models.DateTimeField(default=Delorean(datetime(1970, 1, 1),
                                                    timezone=UTC).datetime)

    rsvps = models.IntegerField(default=0)
    maybe_rsvps = models.IntegerField(default=0)
    waitlist_count = models.IntegerField(default=0)

    status = models.CharField(max_length=255, blank=False)
    visibility = models.CharField(max_length=255, blank=False)

    class Meta:
        ordering = ['time']

    def __str__(self):
        return self.name

    @classmethod
    def future_events(cls):
        today = datetime.now()
        return cls.objects.filter(time__gt=today).filter(time__lt=next_n_months(today, 3))

