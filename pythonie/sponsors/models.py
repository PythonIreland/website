from django.db import models
import logging
import operator
from wagtail.wagtailimages.models import Image

log = logging.getLogger('sponsor')


class SponsorshipLevel(models.Model):
    # level is defined as money spent
    level = models.IntegerField()
    name = models.CharField(max_length=255)

    class Meta:
        ordering = ['-level']

    def __str__(self):
        return self.name


class Sponsor(models.Model):
    name = models.CharField(max_length=255, blank=False)
    description = models.TextField()

    logo = models.ForeignKey(Image)
    url = models.URLField(blank=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    @classmethod
    def for_event(cls, context):
        parents = [page for page in context.get_ancestors(inclusive=True)
                   if hasattr(page, "homepage")]
        homepage = parents[-1].homepage
        all_sponsorship = homepage.homepagesponsorrelationship_set.all()
        return sorted(all_sponsorship, key=operator.attrgetter('level.level'),
                      reverse=True)
