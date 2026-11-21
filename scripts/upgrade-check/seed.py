"""Populate the database with representative content.

Run with the *base* version of the code (before the upgrade) through
`manage.py shell`, so that the upgrade check migrates real, pre-existing data.
"""

import io
import json
import os
import uuid
from datetime import timedelta

from core.models import (
    HomePage,
    HomePageSegment,
    HomePageSponsorRelationship,
    PageSegment,
    SimplePage,
)
from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from django.core.files.images import ImageFile
from django.utils import timezone
from meetups.models import Meetup, MeetupSponsorRelationship
from PIL import Image as PILImage
from sponsors.models import Sponsor, SponsorshipLevel
from wagtail.contrib.redirects.models import Redirect
from wagtail.documents.models import Document
from wagtail.images.models import Image
from wagtail.models import Page, Site

ADMIN_PASSWORD = os.environ.get("UPGRADE_CHECK_ADMIN_PASSWORD", "upgrade-check")
SERVER_PORT = int(os.environ.get("UPGRADE_CHECK_SERVER_PORT", "18000"))

User = get_user_model()
if not User.objects.filter(username="admin").exists():
    User.objects.create_superuser("admin", "admin@example.com", ADMIN_PASSWORD)


def make_image(title, fmt, color):
    buffer = io.BytesIO()
    PILImage.new("RGB", (320, 200), color).save(buffer, fmt)
    buffer.seek(0)
    return Image.objects.create(
        title=title, file=ImageFile(buffer, name=f"{title}.{fmt.lower()}")
    )


png = make_image("logo-png", "PNG", "navy")
webp = make_image("banner-webp", "WEBP", "darkgreen")
document = Document.objects.create(
    title="CoC", file=ContentFile(b"%PDF-1.4 upgrade check", name="coc.pdf")
)

gold = SponsorshipLevel.objects.create(level=1000, name="Gold")
acme = Sponsor.objects.create(
    name="Acme", description="Acme Corp", logo=png, url="https://example.com"
)

# Replace the default Wagtail welcome page with our own tree.
root = Page.objects.get(depth=1)
for page in Page.objects.filter(depth=2):
    page.delete()
root.refresh_from_db()

RICH_TEXT = (
    "<h2>Welcome</h2>"
    "<p>Hello <b>bold</b>, <i>italic</i>, "
    '<a href="https://python.org">ext link</a>, '
    '<a id="{page_id}" linktype="page">internal</a>, '
    f'<a id="{document.id}" linktype="document">doc</a></p>'
    "<ul><li>one</li><li>two</li></ul><ol><li>first</li></ol>"
    f'<embed alt="inline img" embedtype="image" format="fullwidth" id="{png.id}"/>'
)


def stream_body(linked_page_id):
    return json.dumps(
        [
            {"type": "heading", "value": "Python Ireland", "id": str(uuid.uuid4())},
            {
                "type": "paragraph",
                "value": RICH_TEXT.format(page_id=linked_page_id),
                "id": str(uuid.uuid4()),
            },
            {"type": "image", "value": webp.id, "id": str(uuid.uuid4())},
            {"type": "image", "value": png.id, "id": str(uuid.uuid4())},
            {
                "type": "html",
                "value": "<div class='raw-html-marker'>raw</div>",
                "id": str(uuid.uuid4()),
            },
        ]
    )


home = HomePage(
    title="Python Ireland",
    slug="home",
    body="[]",
    show_meetups=True,
    show_sponsors=True,
)
root.add_child(instance=home)
Site.objects.all().delete()
Site.objects.create(
    hostname="127.0.0.1",
    port=SERVER_PORT,
    root_page=home,
    is_default_site=True,
    site_name="pythonie",
)

about = SimplePage(title="About", slug="about", body="[]")
home.add_child(instance=about)
meetups = HomePage(title="Meetups", slug="meetups", body="[]", show_meetups=True)
home.add_child(instance=meetups)
coc = SimplePage(title="Code of Conduct", slug="coc", body="[]")
meetups.add_child(instance=coc)
draft = SimplePage(title="Draft page", slug="draft", body="[]", live=False)
home.add_child(instance=draft)

for page in (home, about, meetups, coc):
    page.body = stream_body(about.id)
    page.save_revision().publish()
draft.body = stream_body(home.id)
draft.save_revision()

segment = PageSegment.objects.create(
    title="Sidebar", body="<p>Segment <b>text</b></p>", location="right"
)
HomePageSegment.objects.create(homepage=home, segment=segment, sort_order=0)
HomePageSponsorRelationship.objects.create(sponsor=acme, homepage=home, level=gold)

now = timezone.now()
meetup = Meetup.objects.create(
    id="m1",
    name="November Meetup",
    description="<p>Talks</p>",
    event_url="https://example.com/m1",
    time=now + timedelta(days=7),
    created=now,
    status="upcoming",
    visibility="public",
)
MeetupSponsorRelationship.objects.create(sponsor=acme, meetup=meetup, note="pizza")
Redirect.objects.create(old_path="/old-about", redirect_page=about)

print(f"Seeded {Page.objects.count()} pages and {Image.objects.count()} images")
