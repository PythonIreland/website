from datetime import datetime, timedelta
import logging

from django.conf import settings
from pytz import UTC
import requests
from meetups import models, schema

log = logging.getLogger(__name__)


def update_not_needed():
    """
    Checks if we need to refresh the meetup events.
    :return: True if a MeetupUpdate exists from the last hour. False otherwise
    """
    an_hour_ago = datetime.now(tz=UTC) - timedelta(hours=1)
    last_checked = models.MeetupUpdate.objects.exclude(updated__lt=an_hour_ago).exists()
    return last_checked


def get_content(url, params=None):
    response = requests.get(url, params=params)
    log.debug("Retrieved {} from {}".format(response.json(), url))
    return response.json()


def update():
    """ Contacts meetup.com API to retrieve meetup data
    """
    if update_not_needed():
        log.info("Not updating meetups")
        return
    log.info("Updating meetups")
    meetup_data = get_content(
        'https://api.meetup.com/2/events.html',
        params={'key': settings.MEETUP_KEY,
                'group_urlname': 'pythonireland',
                'text_format': 'html',
                'time': ',3m'})
    log.info(meetup_data)
    meetups = schema.Meetups()
    meetups = meetups.deserialize(meetup_data)
    log.info(meetups)
    for result in meetups.get('results'):
        # Check if the meetup exists
        meetup = models.Meetup.objects.filter(id=result['id']).first() or models.Meetup()
        meetup.rsvps = result.get('yes_rsvp_count')
        meetup.maybe_rsvps = result.get('maybe_rsvp_count')
        meetup.waitlist_count = result.get('waitlist_count')

        if result['updated'] <= meetup.updated:
            log.info('Existing meetup:{!r} RSPs updated'.format(meetup))
            meetup.save()
            continue

        meetup.id = result.get('id')
        meetup.visibility = result.get('visibility')
        meetup.created = result.get('created')
        meetup.name = result.get('name')
        meetup.description = result.get('description')
        meetup.event_url = result.get('event_url')
        meetup.time = result.get('time')
        meetup.updated = result.get('updated')
        meetup.status = result.get('status')
        meetup.visibility = result.get('visibility')
        meetup.save()
        models.MeetupUpdate.tick()
        log.info('Existing meetup:{!r} fully updated'.format(meetup))
