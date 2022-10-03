import enum
import logging

import numpy as np
import pandas as pd
from django.core.management.base import BaseCommand, CommandParser
from django.utils.text import slugify
from wagtail.core.models import Page

from speakers.models import Speaker, Room, Session

log = logging.getLogger("import-sessionize")


class SessionHeaders(str, enum.Enum):
    Id = "Session Id"
    Title = "Title"
    Description = "Description"
    OwnerInformed = "Owner Informed"
    OwnerConfirmed = "Owner Confirmed"
    Room = "Room"
    ScheduledAt = "Scheduled At"
    ScheduledDuration = "Scheduled Duration"
    SpeakerIds = "Speaker Ids"


class SpeakerHeaders(str, enum.Enum):
    Id = "Speaker Id"
    FirstName = "FirstName"
    LastName = "LastName"
    Email = "Email"
    TagLine = "TagLine"
    Bio = "Bio"
    ProfilePicture = "Profile Picture"
    Blog = "Blog"
    Twitter = "Twitter"
    LinkedIn = "LinkedIn"


SESSION_HEADERS = [member.value for name, member in SessionHeaders.__members__.items()]
print(f"{SESSION_HEADERS=}")
SPEAKER_HEADERS = [member.value for name, member in SpeakerHeaders.__members__.items()]
print(f"{SPEAKER_HEADERS=}")


class Command(BaseCommand):
    help = "Import the sessionize record"

    def add_arguments(self, parser: CommandParser):
        parser.add_argument("--file", "-f", action="store", type=str)

    def handle(self, *args, **options):
        self.save_speakers(options)
        self.save_sessions(options)

    def save_speakers(self, options):
        df_accepted_speakers = pd.read_excel(
            options["file"],
            sheet_name="Accepted speakers",
        )
        speakers = df_accepted_speakers[SPEAKER_HEADERS]
        parent_page = Page.objects.get(id=144).specific
        print(parent_page.title)
        for index, row in speakers.iterrows():
            # print(index, row)
            name = f"{row[SpeakerHeaders.FirstName]} {row[SpeakerHeaders.LastName]}"
            print(f"{row[SpeakerHeaders.Id]=}")
            picture_url = row[SpeakerHeaders.ProfilePicture]
            if picture_url is np.nan:
                picture_url = ""
            try:
                speaker = Speaker.objects.get(external_id=row[SpeakerHeaders.Id])
                speaker.name = name
                speaker.email = row[SpeakerHeaders.Email]
                speaker.biography = row[SpeakerHeaders.Bio]
                speaker.picture_url = picture_url
                speaker.title = name
            except Speaker.DoesNotExist:
                speaker = Speaker(
                    external_id=row[SpeakerHeaders.Id],
                    name=name,
                    email=row[SpeakerHeaders.Email],
                    biography=row[SpeakerHeaders.Bio],
                    picture_url=picture_url,
                    title=name,
                )
                parent_page.add_child(instance=speaker)

            speaker.save()
            speaker.save_revision().publish()

    def save_sessions(self, options):
        df_accepted_session = pd.read_excel(
            options["file"],
            sheet_name="Accepted sessions",
        )
        sessions = df_accepted_session[SESSION_HEADERS]
        parent_page = Page.objects.get(id=145).specific

        for index, row in sessions.iterrows():

            if row[SessionHeaders.Room] is np.nan:
                continue

            room, created = Room.objects.get_or_create(
                name=row[SessionHeaders.Room],
            )

            if row[SessionHeaders.ScheduledAt] is pd.NaT:
                continue

            state = Session.StateChoices.ACCEPTED
            if row[SessionHeaders.OwnerConfirmed] != "No":
                state = Session.StateChoices.CONFIRMED

            session_type = Session.TypeChoices.TALK
            if str(row[SessionHeaders.Title]).startswith("Workshop:"):
                session_type = Session.TypeChoices.WORKSHOP

            name = row[SessionHeaders.Title]

            print(f"{row[SessionHeaders.Id]=}")
            try:
                session = Session.objects.get(external_id=row[SessionHeaders.Id])
                session.name = name
                session.description = row[SessionHeaders.Description]
                session.room = room
                session.scheduled_at = row[SessionHeaders.ScheduledAt]
                session.duration = row[SessionHeaders.ScheduledDuration]
                session.state = state
                session.type = session_type
                session.title = name
            except Session.DoesNotExist:
                session = Session(
                    external_id=row[SessionHeaders.Id],
                    name=name,
                    description=row[SessionHeaders.Description],
                    room=room,
                    scheduled_at=row[SessionHeaders.ScheduledAt],
                    duration=row[SessionHeaders.ScheduledDuration],
                    state=state,
                    type=session_type,
                    title=name,
                )
                parent_page.add_child(instance=session)

            session.save()
            session.save_revision().publish()

            session.speakers.all().delete()
            session.save()

            speaker_ids = [
                speaker_id.strip()
                for speaker_id in row[SessionHeaders.SpeakerIds].split(",")
            ]
            for speaker in Speaker.objects.filter(external_id__in=speaker_ids):
                session.speakers.add(speaker)

            session.save()


# print(f"{session_speakers=}")
