import factory
from django.utils import timezone
from factory.django import DjangoModelFactory
from meetups.models import Meetup
from sponsors.models import SponsorshipLevel

from core.models import HomePage, SimplePage


class SponsorshipLevelFactory(DjangoModelFactory):
    class Meta:
        model = SponsorshipLevel
        django_get_or_create = ("name",)

    level = 100
    name = "Bronze"


class MeetupFactory(DjangoModelFactory):
    class Meta:
        model = Meetup
        django_get_or_create = ("id",)

    id = factory.Sequence(lambda n: f"meetup-{n}")
    name = "Python Ireland Meetup"
    description = "Monthly Python meetup in Dublin"
    event_url = "https://meetup.com/pythonireland/"
    time = factory.LazyFunction(lambda: timezone.now() + timezone.timedelta(days=30))
    created = factory.LazyFunction(timezone.now)
    rsvps = 50
    status = "upcoming"
    visibility = "public"


class HomePageFactory(DjangoModelFactory):
    class Meta:
        model = HomePage

    title = "Python Ireland"
    slug = "home"
    show_meetups = True
    body = []


class SimplePageFactory(DjangoModelFactory):
    class Meta:
        model = SimplePage

    title = "Sample Page"
    slug = "sample-page"
    body = []
