import logging
from django.core.management.base import BaseCommand
from speakers.models import SpeakersPage
from speakers.models import TalksPage

log = logging.getLogger('speakers')


class Command(BaseCommand):
    help = 'Updates the speakers and talks from lanyrd'

    def handle(self, *args, **options):
        speaker_pages = SpeakersPage.objects.all()
        for speaker_page in speaker_pages:
            if speaker_page.api_url:
                log.info('api_url: %s' % speaker_page.api_url)
                speaker_page.fetch()
                self.stdout.write('Successfully fetched speakers')

        talk_pages = TalksPage.objects.all()
        for talk_page in talk_pages:
            if talk_page.api_url:
                log.info('api_url: %s' % talk_page.api_url)
                talk_page.fetch()
                self.stdout.write('Successfully fetched talks')
