from unittest.mock import patch

from django.test import TestCase

from model_mommy import mommy

from meetups import utils

from meetups.models import Meetup


class MeetupModelTests(TestCase):
    def test_create_meetup(self):
        meetup = mommy.make(Meetup)
        self.assertIsNotNone(meetup.id)


class UtilsTests(TestCase):
    @patch('meetups.utils.get_content')
    def test_update_first_run(self, mock_get_content):
        mock_get_content.return_value = {
            'results': [
                {
                    'maybe_rsvp_count': 0,
                    'id': 'qwfbshytjbnb',
                    'waitlist_count': 0,
                    'yes_rsvp_count': 24,
                    'utc_offset': 3600000,
                    'visibility': 'public',
                    'announced': False,
                    'updated': 1431467590000,
                    'description': '<p>We will be having a meetup in June. More details to follow.</p> <p>If you are interested in speaking, please submit your details to\xa0<a href="http://bit.ly/pyie-cfp-2015"><a href="http://bit.ly/pyie-cfp-2015" class="linkified">http://bit.ly/pyie-cfp-2015</a></a>.</p> <p>Enquiries? Please contact contact@python.ie.</p>',
                    'name': 'Python Ireland meetup',
                    'event_url': 'http://www.meetup.com/pythonireland/events/221078098/',
                    'headcount': 0,
                    'time': 1433957400000,
                    'created': 1390942022000,
                    'group': {
                        'name': 'Python Ireland',
                        'id': 6943212,
                        'who': 'Pythonista',
                        'join_mode': 'open',
                        'created': 1359572645000,
                        'group_lon': -6.25,
                        'group_lat': 53.33000183105469,
                        'urlname': 'pythonireland'
                    },
                    'status': 'upcoming'
                }
            ]
        }
        utils.update()
        meetups = Meetup.objects.all()
        self.assertEqual(len(meetups), 1)

