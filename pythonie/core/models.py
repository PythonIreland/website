from __future__ import unicode_literals

from django.db import models
from modelcluster.fields import ParentalKey

from wagtail.wagtailadmin.edit_handlers import FieldPanel, InlinePanel
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailcore.models import Page, Orderable
from wagtail.wagtailsnippets.edit_handlers import SnippetChooserPanel
from wagtail.wagtailsnippets.models import register_snippet

from wagtailnews.models import NewsIndexMixin, AbstractNewsItem
from wagtailnews.decorators import newsindex

import logging
from meetups.models import Meetup
from meetups.utils import update

log = logging.getLogger('pythonie')


@register_snippet
class PageSegment(models.Model):
    title = models.CharField(max_length=255)
    body = RichTextField()
    location = models.CharField(
        max_length=5,
        choices=(('main', 'Main section'), ('right', 'Right side'), ('left', 'Left side')),
        default='main')

    panels = [
        FieldPanel('title', classname='full title'),
        FieldPanel('body', classname='full'),
        FieldPanel('location', classname='select'),
    ]

    def __str__(self):
        return "{!s} on {!s}".format(self.title, self.homepage_segments.first())


class HomePageSegment(Orderable, models.Model):
    homepage = ParentalKey('HomePage', related_name='homepage_segments')
    segment = models.ForeignKey('PageSegment', related_name='homepage_segments')

    class Meta:
        verbose_name = "Homepage Segment"
        verbose_name_plural = "Homepage Segments"

    panels = [
        SnippetChooserPanel('segment', PageSegment),
    ]

    def __str__(self):
        return "{!s} Segment".format(self.homepage)


class HomePage(Page):
    subpage_types = ['NewsIndex', 'HomePage']

    def segments_for_location(self, location):
        return self.homepage_segments.filter(segment__location=location)

    def segments_for_main(self):
        return self.segments_for_location('main')

    def segments_for_right(self):
        return self.segments_for_location('right')

    @staticmethod
    def menu_items():
        """ Get child pages of this HomePage which have 'show_in_menu' set to True and are published.
        """
        return Page.objects.live().in_menu()

    def news_items(self):
        news_index = NewsIndex.objects.child_of(self).first()
        if not news_index:
            return []
        news_items = news_index.newsitem_set.all()
        return news_items

    def meetups(self):
        update()
        meetups = Meetup.objects.all()
        return meetups

    def __str__(self):
        return self.title


HomePage.content_panels = HomePage.content_panels + [
    InlinePanel('homepage_segments', label='Homepage Segment'),
]


# The decorator registers this model as a news index
@newsindex
class NewsIndex(NewsIndexMixin, Page):
    # Add extra fields here, as in a normal Wagtail Page class, if required
    newsitem_model = 'NewsItem'


class NewsItem(AbstractNewsItem):
    # NewsItem is a normal Django model, *not* a Wagtail Page.
    # Add any fields required for your page.
    # It already has ``date`` field, and a link to its parent ``NewsIndex`` Page
    title = models.CharField(max_length=255)
    body = RichTextField()

    panels = [FieldPanel('title', classname='full title'),
              FieldPanel('body', classname='full'), ] + AbstractNewsItem.panels

    def __unicode__(self):
        return self.title
