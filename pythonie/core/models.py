from __future__ import unicode_literals

from django.db import models
from modelcluster.fields import ParentalKey

from wagtail.wagtailadmin.edit_handlers import FieldPanel, InlinePanel
from wagtail.wagtailcore.blocks import RawHTMLBlock
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailcore.models import Page, Orderable
from wagtail.wagtailsnippets.edit_handlers import SnippetChooserPanel
from wagtail.wagtailsnippets.models import register_snippet

from wagtailnews.models import NewsIndexMixin, AbstractNewsItem
from wagtailnews.decorators import newsindex

from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailcore import blocks
from wagtail.wagtailadmin.edit_handlers import StreamFieldPanel
from wagtail.wagtailimages.blocks import ImageChooserBlock
from wagtail.wagtailembeds.blocks import EmbedBlock

from sponsors.models import Sponsor, SponsorshipLevel

import logging

log = logging.getLogger('pythonie')


class MeetupMixin(models.Model):
    show_meetups = models.BooleanField(default=False)

    settings_panels = [
        FieldPanel('show_meetups'),
    ]

    class Meta:
        abstract = True


class SponsorMixin(models.Model):
    show_sponsors = models.BooleanField(default=False)

    settings_panels = [
        FieldPanel('show_sponsors'),
    ]

    class Meta:
        abstract = True


@register_snippet
class PageSegment(models.Model):
    """ This is a fixed text content
    """
    title = models.CharField(max_length=255)
    body = RichTextField()
    location = models.CharField(
        max_length=5,
        choices=(('main', 'Main section'),
                 ('right', 'Right side'),
                 ('left', 'Left side')),
        default='main')

    panels = [
        FieldPanel('title', classname='full title'),
        FieldPanel('body', classname='full'),
        FieldPanel('location', classname='select'),
    ]

    def __str__(self):
        return "{!s} on {!s}".format(self.title,
                                     self.homepage_segments.first())


class HomePageSegment(Orderable, models.Model):
    """ Pivot table to associate a HomePage to Segment snippets
    """
    homepage = ParentalKey('HomePage', related_name='homepage_segments')
    segment = models.ForeignKey('PageSegment',
                                related_name='homepage_segments')

    class Meta:
        verbose_name = "Homepage Segment"
        verbose_name_plural = "Homepage Segments"

    panels = [
        SnippetChooserPanel('segment', PageSegment),
    ]

    def __str__(self):
        return "{!s} Segment".format(self.homepage)


class HomePageSponsorRelationship(models.Model):
    """ Qualify how sponsor helped content described in HomePage
    Pivot table for Sponsor M<-->M HomePage
    """
    sponsor = models.ForeignKey(Sponsor)
    homepage = models.ForeignKey('HomePage')
    level = models.ForeignKey(SponsorshipLevel)

    def __repr__(self):
        return '{} {} {}'.format(self.sponsor.name,
                                 self.homepage.title,
                                 self.level.name)


class HomePage(Page, MeetupMixin, SponsorMixin):
    subpage_types = ['HomePage', 'SimplePage',
                     'speakers.SpeakersPage', 'speakers.TalksPage']

    body = StreamField([
        ('heading', blocks.CharBlock(icon="home",
                                     classname="full title")),
        ('paragraph', blocks.RichTextBlock(icon="edit")),
        ('video', EmbedBlock(icon="media")),
        ('image', ImageChooserBlock(icon="image")),
        ('slide', EmbedBlock(icon="media")),
        ('html', RawHTMLBlock(icon="code"))
    ])

    sponsors = models.ManyToManyField(Sponsor,
                                      through=HomePageSponsorRelationship,
                                      blank=True)

    def __str__(self):
        return self.title

    content_panels = Page.content_panels + [
        StreamFieldPanel('body'),
    ]

    settings_panels = (Page.settings_panels + MeetupMixin.settings_panels +
                       SponsorMixin.settings_panels +
                       [InlinePanel('homepage_segments',
                                    label='Homepage Segment')])


class SimplePage(Page, MeetupMixin, SponsorMixin):
    """
    allowed url to embed listed in
    lib/python3.4/site-packages/wagtail/wagtailembeds/oembed_providers.py
    """
    body = StreamField([
        ('heading', blocks.CharBlock(icon="home",
                                     classname="full title")),
        ('paragraph', blocks.RichTextBlock(icon="edit")),
        ('video', EmbedBlock(icon="media")),
        ('image', ImageChooserBlock(icon="image")),
        ('slide', EmbedBlock(icon="media")),
        ('html', RawHTMLBlock(icon="code"))
    ])

    content_panels = Page.content_panels + [
        StreamFieldPanel('body'),
    ]

    settings_panels = (Page.settings_panels + MeetupMixin.settings_panels +
                       SponsorMixin.settings_panels)


@newsindex
class NewsIndex(NewsIndexMixin, Page):
    # Add extra fields here, as in a normal Wagtail Page class, if required
    newsitem_model = 'NewsItem'


class NewsItem(AbstractNewsItem):
    """
    NewsItem is a normal Django model, *not* a Wagtail Page.
    Add any fields required for your page.
    It already has ``date`` field, and a link to its parent ``NewsIndex`` Page
    """
    title = models.CharField(max_length=255)
    body = RichTextField()

    panels = [FieldPanel('title', classname='full title'),
              FieldPanel('body', classname='full'), ] + AbstractNewsItem.panels

    def __unicode__(self):
        return self.title
