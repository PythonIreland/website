from django.test import TestCase

from model_mommy import mommy

from sponsors.models import Sponsor

class SponsorModelTests(TestCase):
    def test_create_sponsor(self):
        sponsor = mommy.make(Sponsor)
        self.assertIsNotNone(sponsor.id)
        self.assertIsNotNone(sponsor.name)
        self.assertIsNotNone(sponsor.logo)

