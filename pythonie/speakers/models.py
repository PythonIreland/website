import json
import logging

import requests
from django.conf import settings
from django.db import models
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.core.models import Page

log = logging.getLogger("speakers")


class Room(models.Model):
    name = models.CharField(max_length=255, blank=False)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]


class Speaker(Page):
    name = models.CharField(max_length=255, blank=False)
    email = models.CharField(max_length=255, blank=False)
    external_id = models.CharField(max_length=255, unique=True, blank=True)
    picture_url = models.CharField(max_length=255, blank=True)
    biography = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    content_panels = Page.content_panels + [
        FieldPanel("name"),
        FieldPanel("email"),
        FieldPanel("external_id"),
        FieldPanel("biography"),
        FieldPanel("picture_url"),
    ]

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]


class SpeakersPage(Page):
    subpage_types = ["Speaker"]

    @property
    def speakers(self):
        return Speaker.objects.order_by("name").all()


# In this context, a session is a link to a future proposal (talk)
class Session(Page):
    class StateChoices(models.TextChoices):
        DRAFT = "draft", "Draft"
        ACCEPTED = "accepted", "Accepted"
        CONFIRMED = "confirmed", "Confirmed"
        REFUSED = "refused", "Refused"
        CANCELLED = "cancelled", "Cancelled"

    class TypeChoices(models.TextChoices):
        TALK = "talk", "Talk"
        WORKSHOP = "workshop", "Workshop"

    name = models.CharField(max_length=255, blank=False, db_index=True)
    description = models.TextField()
    scheduled_at = models.DateTimeField()
    duration = models.IntegerField(default=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    external_id = models.CharField(max_length=255, unique=True)
    type = models.CharField(
        max_length=16,
        blank=False,
        choices=TypeChoices.choices,
        default=TypeChoices.TALK,
        db_index=True,
    )

    state = models.CharField(
        max_length=16,
        blank=False,
        choices=StateChoices.choices,
        default=StateChoices.DRAFT,
        db_index=True,
    )
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    # speaker = models.ForeignKey(Speaker, on_delete=models.CASCADE)
    speakers = models.ManyToManyField(Speaker, related_name="sessions")

    @property
    def speaker_names(self):
        return ', '.join(speaker.name for speaker in self.speakers.all())

    content_panels = Page.content_panels + [
        FieldPanel("name"),
        FieldPanel("description"),
        FieldPanel("scheduled_at"),
        FieldPanel("duration"),
        FieldPanel("type"),
        FieldPanel("state"),
    ]

    def is_confirmed(self) -> bool:
        return self.state == "confirmed"

    def __str__(self):
        return self.name

    class Meta:
        ordering = [
            "name",
        ]


class TalksPage(Page):
    subpage_types = ["Session"]

    @property
    def sessions(self):
        return Session.objects.order_by("scheduled_at", "room__name").all()
