from django.core.management.base import BaseCommand
from meetups.utils import update


class Command(BaseCommand):
    help = 'Updates the details from meetup'

    def handle(self, *args, **options):
        update()
