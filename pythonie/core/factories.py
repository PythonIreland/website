from django.utils import timezone
import wagtail_factories

from core.models import HomePage, SimplePage
from meetups.models import Meetup
from sponsors.models import SponsorshipLevel


def create_sponsorship_level(name="Bronze", level=100):
    return SponsorshipLevel.objects.get_or_create(name=name, defaults={"level": level})[
        0
    ]


def create_meetup(
    id,
    name="Python Ireland Meetup",
    description="Monthly Python meetup in Dublin",
    event_url="https://meetup.com/pythonireland/",
    time=None,
    created=None,
    rsvps=50,
    status="upcoming",
    visibility="public",
):
    if time is None:
        time = timezone.now() + timezone.timedelta(days=30)
    if created is None:
        created = timezone.now()

    return Meetup.objects.get_or_create(
        id=id,
        defaults={
            "name": name,
            "description": description,
            "event_url": event_url,
            "time": time,
            "created": created,
            "rsvps": rsvps,
            "status": status,
            "visibility": visibility,
        },
    )[0]


class HomePageFactory(wagtail_factories.PageFactory):
    class Meta:
        model = HomePage

    title = "Python Ireland"
    slug = "home"
    show_meetups = True
    body = []


class SimplePageFactory(wagtail_factories.PageFactory):
    class Meta:
        model = SimplePage

    title = "Sample Page"
    slug = "sample-page"
    body = []


def SponsorshipLevelFactory(name="Bronze", level=100):
    return create_sponsorship_level(name=name, level=level)


def MeetupFactory(id, name="Python Ireland Meetup", **kwargs):
    return create_meetup(id=id, name=name, **kwargs)
