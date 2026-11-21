from django.test import TestCase
from model_bakery import baker

from sponsors.models import Sponsor, SponsorshipLevel


class SponsorModelTests(TestCase):
    def test_create_sponsor(self):
        sponsor = baker.make(Sponsor)
        self.assertIsNotNone(sponsor.id)
        self.assertIsNotNone(sponsor.description)
        self.assertIsNotNone(sponsor.name)
        self.assertIsNotNone(sponsor.logo)
        self.assertIsNotNone(sponsor.url)


class SponsorshipLevelModelTests(TestCase):
    def test_create_sponsorshiplevel(self):
        sponsorship = baker.make(SponsorshipLevel)
        self.assertIsNotNone(sponsorship.id)
        self.assertIsNotNone(sponsorship.name)
        self.assertIsNotNone(sponsorship.level)
