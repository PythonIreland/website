from django.core.management.base import BaseCommand
from wagtail.models import Page, Site

from core.factories import (
    HomePageFactory,
    MeetupFactory,
    SimplePageFactory,
    SponsorshipLevelFactory,
)
from core.models import HomePage, SimplePage


class Command(BaseCommand):
    help = "Generate sample data for development"

    def handle(self, *args, **options):
        self.stdout.write("Generating sample data...")

        self._create_sponsorship_levels()
        self._create_meetups()
        home = self._create_home_page()
        self._create_navigation_pages(home)

        self.stdout.write(self.style.SUCCESS("\nSample data generated successfully!"))

    def _create_sponsorship_levels(self):
        levels = [("Bronze", 100), ("Silver", 200), ("Gold", 300), ("Platinum", 400)]
        for name, level in levels:
            SponsorshipLevelFactory(name=name, level=level)
        self.stdout.write(self.style.SUCCESS("Created sponsorship levels"))

    def _create_meetups(self):
        names = ["Python Ireland Monthly Meetup", "Django Dublin", "PyData Ireland"]
        for i, name in enumerate(names):
            MeetupFactory(id=f"meetup-{i}", name=name)
        self.stdout.write(self.style.SUCCESS("Created meetups"))

    def _create_home_page(self):
        home = HomePage.objects.first()
        if home:
            self.stdout.write("Home page already exists")
            return home

        wagtail_root = Page.objects.get(depth=1)
        default_home_exists = Page.objects.filter(slug="home", depth=2).exists()
        slug = "python-ireland" if default_home_exists else "home"

        home = HomePageFactory.build(
            slug=slug,
            show_in_menus=True,
            body=self._get_home_content(),
        )
        wagtail_root.add_child(instance=home)
        self.stdout.write(self.style.SUCCESS("Created home page"))

        site = Site.objects.filter(is_default_site=True).first()
        if site:
            site.root_page = home
            site.save()
            self.stdout.write(self.style.SUCCESS("Updated site root page"))

        return home

    def _create_navigation_pages(self, home):
        pycon = self._create_page(home, "PyCon 2025", "pycon-2025")
        self._create_page(pycon, "Schedule", "schedule")
        self._create_page(pycon, "Speakers", "pycon-speakers")
        self._create_page(pycon, "Sponsors", "pycon-sponsors")
        self._create_page(pycon, "Venue", "venue")
        self._create_page(pycon, "Tickets", "tickets")

        self._create_page(home, "Meetups", "meetups", self._get_meetups_content())
        self._create_page(home, "Learning Resources", "learning-resources")

        previous = self._create_page(home, "Previous PyCons", "previous-pycons")
        for year in [2024, 2023, 2022, 2019]:
            self._create_page(previous, f"PyCon {year}", f"pycon-{year}")

        self._create_page(home, "Coaching program", "coaching-program")
        self._create_page(home, "About", "about")

        policies = self._create_page(home, "Policies", "policies")
        self._create_page(policies, "Code of Conduct", "code-of-conduct")
        self._create_page(policies, "Privacy Policy", "privacy-policy")
        self._create_page(policies, "Cookie Policy", "cookie-policy")

    def _create_page(self, parent, title, slug, body=None):
        if SimplePage.objects.filter(slug=slug).exists():
            self.stdout.write(f"  {title} already exists")
            return SimplePage.objects.get(slug=slug)

        page = SimplePageFactory.build(
            title=title, slug=slug, body=body or [], show_in_menus=True
        )
        parent.add_child(instance=page)
        self.stdout.write(self.style.SUCCESS(f"Created {title}"))
        return page

    def _get_home_content(self):
        return [
            {"type": "heading", "value": "Introduction"},
            {
                "type": "paragraph",
                "value": (
                    "<p>Python Ireland is the Irish organisation representing the various chapters of Python users. "
                    "We organise meet ups and events for software developers, students, academics and anyone who wants "
                    "to learn the language. One of our aims is to help grow and diversify the Python community in Ireland. "
                    "We also develop and foster links with other Python based communities overseas.</p>"
                ),
            },
            {"type": "heading", "value": "PyCon Ireland 2025"},
            {
                "type": "paragraph",
                "value": (
                    "<p>We are thrilled to announce PyCon Ireland 2025, taking place in Dublin "
                    "on November 15th and 16th! Join us at the UCD O'Reilly Hall for this exciting event.</p>"
                ),
            },
            {
                "type": "paragraph",
                "value": (
                    "<p>PyCon Ireland 2025 will feature two talk tracks and two workshop tracks on both days. "
                    "Your ticket includes breakfast and lunch. Join us Saturday evening for networking!</p>"
                ),
            },
            {
                "type": "paragraph",
                "value": (
                    "<p>Please adhere to our <a href='/policies/code-of-conduct/'>Code of Conduct</a>. "
                    "Check <a href='/pycon-2025/'>Terms and conditions</a> for details.</p>"
                ),
            },
            {"type": "paragraph", "value": "<p>See you at PyCon Ireland 2025!</p>"},
        ]

    def _get_meetups_content(self):
        return [
            {"type": "heading", "value": "Python Ireland Meetups"},
            {
                "type": "paragraph",
                "value": (
                    "<p>Join us at our regular meetups! We hold events every month.</p>"
                    "<ul>"
                    "<li><a href='https://www.meetup.com/pythonireland/events/'>Upcoming Events</a></li>"
                    "<li><a href='https://www.meetup.com/pythonireland/photos/'>Photos</a></li>"
                    "<li><a href='https://www.meetup.com/pythonireland/'>Python Ireland on Meetup.com</a></li>"
                    "</ul>"
                ),
            },
        ]
