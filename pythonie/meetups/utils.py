from datetime import datetime, timedelta
import logging

from django.conf import settings
import requests
from meetups import models, schema


log = logging.getLogger(__name__)


def update_needed():
    an_hour_ago = datetime.now() - timedelta(hours=1)
    last_checked = models.MeetupUpdate.objects.filter(models.MeetupUpdate.updated < an_hour_ago).exists()
    return last_checked


def get_content(url, params=None):
    response = requests.get(url, params=params)
    log.debug("Retrieved {} from {}".format(response.json(), url))
    return response.json()


def update():
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
    for result in meetups['results']:
        # Check if the meetup exists
        meetup = models.Meetup.objects.filter(id=result['id']).first()
        if meetup:
            if result['updated'] <= meetup.updated:
                log.info('Not updating existing meetup:{!r} as there is nothing to update'.format(meetup))
                continue
        meetup = models.Meetup()
        meetup.id = result.get_value('id')
        meetup.announced = result.get_value('announced')
        meetup.created = result.get_value('created')
