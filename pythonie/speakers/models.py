import json
import logging
import requests

from django.conf import settings
from django.db import models

from wagtail.wagtailadmin.edit_handlers import FieldPanel
from wagtail.wagtailcore.models import Page

log = logging.getLogger('speakers')


class SpeakersPage(Page):
    api_url = models.CharField(max_length=255, blank=False)

    settings_panels = Page.settings_panels + [
        FieldPanel('api_url', classname="full"),
    ]

    def fetch(self):
        log.info('api_url=%s' % self.api_url)
        response = requests.get(self.api_url)
        log.info('api_response=%r' % response)
        settings.REDIS.set(self.api_url, response.content)
        log.info('Speakers saved in redis with key=%s' % self.api_url)

    @property
    def speakers(self):
        log.info('Fetching from redis_url=%s with key=%s' % (
            settings.REDIS_URL, self.api_url))
        result = settings.REDIS.get(self.api_url)
        decoded = result.decode("utf-8")
        result = json.loads(decoded)
        log.info('Speakers fetched from redis: %r' % result)
        return sorted(result.get('speakers'), key=lambda x: x.get('name'))


class TalksPage(Page):
    api_url = models.CharField(max_length=255, blank=False)

    settings_panels = Page.settings_panels + [
        FieldPanel('api_url', classname="full"),
    ]

    def fetch(self):
        log.info('api_url=%s' % self.api_url)
        response = requests.get(self.api_url)
        log.info('api_response=%r' % response)
        settings.REDIS.set(self.api_url, response.content)
        log.info('Talks saved in redis with key=%s' % self.api_url)

    @property
    def schedule(self):
        log.info('Fetching from redis_url=%s with key=%s' % (
            settings.REDIS_URL, self.api_url))
        result = settings.REDIS.get(self.api_url)
        decoded = result.decode("utf-8")
        result = json.loads(decoded)
        log.info('Talks fetched from redis: %r' % result)
        return result

    @property
    def day_1(self):
        return self.schedule['sessions'][0]['sessions']

    @property
    def day_2(self):
        return self.schedule['sessions'][1]['sessions']
