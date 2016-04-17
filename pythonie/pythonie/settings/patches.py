"""
Run once, good place to patch 3rd party apps
"""

import logging

# allow for other slideshare urls (fr.slideshare...)
from wagtail.wagtailembeds import oembed_providers
from wagtail.wagtailembeds.oembed_providers import compile_endpoints
from wagtail.wagtailembeds.oembed_providers import OEMBED_ENDPOINTS

log = logging.getLogger('pythonie')

log.info("Patching wagtail.wagtailembeds.oembed_providers")
OEMBED_ENDPOINTS.update({
    "https://www.slideshare.net/api/oembed/2": [
        "^http://.+\\.slideshare\\.net/.+$"
    ], })
oembed_providers.OEMBED_ENDPOINTS = OEMBED_ENDPOINTS
oembed_providers.OEMBED_ENDPOINTS_COMPILED = compile_endpoints()
