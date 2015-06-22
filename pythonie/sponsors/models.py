from datetime import datetime, timedelta
from django.db import models

import logging
from pytz import UTC

from wagtail.wagtailimages.models import Image


log = logging.getLogger('sponsor')


class Sponsor(models.Model):
    name = models.CharField(max_length=255, blank=False)
    description = models.TextField()

    logo = models.ForeignKey(Image)

    is_active = models.BooleanField(default=False)
    status = models.CharField(max_length=255, blank=False)
    visibility = models.CharField(max_length=255, blank=False)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

