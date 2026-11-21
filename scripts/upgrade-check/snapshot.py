"""Render the public pages and save their HTML, to diff before/after upgrade.

Run through `manage.py shell`. The output directory is given by the
UPGRADE_CHECK_SNAPSHOT environment variable.
"""

import os
import re
from pathlib import Path

from django.test import Client

output = Path(os.environ["UPGRADE_CHECK_SNAPSHOT"])
output.mkdir(parents=True, exist_ok=True)
port = os.environ.get("UPGRADE_CHECK_SERVER_PORT", "18000")
client = Client(HTTP_HOST=f"127.0.0.1:{port}")

PAGES = [
    ("home", "/"),
    ("about", "/about/"),
    ("meetups", "/meetups/"),
    ("coc", "/meetups/coc/"),
    ("redirect", "/old-about"),
    ("missing", "/nope/"),
]

for name, url in PAGES:
    response = client.get(url)
    html = response.content.decode()
    html = re.sub(r'csrfmiddlewaretoken" value="[^"]+"', "csrf", html)
    (output / f"{name}.html").write_text(html)
    location = response.get("Location", "")
    print(f"  {name:<9} {response.status_code} {location}")
