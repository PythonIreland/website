import datetime

import pydantic
import requests
from django.core.management import BaseCommand, CommandParser
from wagtail.core.models import Page

from speakers.models import Speaker, Session, Room


class SessionModel(pydantic.BaseModel):
    id: str
    title: str
    description: str
    startsAt: datetime.datetime
    endsAt: datetime.datetime
    speakers: list[pydantic.UUID4]
    roomId: int

    @property
    def duration(self) -> int:
        return int((self.endsAt - self.startsAt).seconds / 60)


class SpeakerModel(pydantic.BaseModel):
    id: pydantic.UUID4
    firstName: str
    lastName: str
    bio: str | None
    tagLine: str
    profilePicture: pydantic.HttpUrl | None
    sessions: list[int]
    fullName: str
    # email: str

    # @property
    # def fullName(self):
    #     return f'{self.firstName} {self.lastName}'


class RoomModel(pydantic.BaseModel):
    id: int
    name: str


class SessionizeModel(pydantic.BaseModel):
    sessions: list[SessionModel]
    speakers: list[SpeakerModel]
    rooms: list[RoomModel]


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        response = requests.get("https://sessionize.com/api/v2/z66z4kb6/view/All")
        sessionize: SessionizeModel = SessionizeModel.parse_obj(response.json())

        rooms = {}

        for incoming_room in sessionize.rooms:
            incoming_room: RoomModel
            rooms[incoming_room.id] = self.save_room(incoming_room)

        parent_page: Page = Page.objects.get(id=144).specific
        for speaker in sessionize.speakers:
            speaker: SpeakerModel
            self.save_speaker(parent_page, speaker)

        parent_page: Page = Page.objects.get(id=145).specific
        for session in sessionize.sessions:
            session: SessionModel
            self.save_session(parent_page, rooms[session.roomId], session)

    def save_speaker(self, parent_page: Page, incoming_speaker: SpeakerModel) -> None:
        print(f"{incoming_speaker.id} {incoming_speaker.fullName}")
        try:
            speaker: Speaker = Speaker.objects.get(external_id=incoming_speaker.id)
            speaker.name = incoming_speaker.fullName
            speaker.email = f"{incoming_speaker.id}@sessionize.com"
            speaker.biography = incoming_speaker.bio or "No biography available."
            speaker.picture_url = incoming_speaker.profilePicture or ""
            speaker.title = incoming_speaker.fullName
        except Speaker.DoesNotExist:
            speaker: Speaker = Speaker(
                external_id=incoming_speaker.id,
                name=incoming_speaker.fullName,
                email=f"{incoming_speaker.id}@sessionize.com",
                biography=incoming_speaker.bio or "No biography available",
                picture_url=incoming_speaker.profilePicture or "",
                title=incoming_speaker.fullName,
            )

            parent_page.add_child(instance=speaker)

        speaker.save()
        speaker.save_revision().publish()

    def save_session(
        self,
        parent_page: Page,
        room: Room,
        incoming_session: SessionModel,
    ) -> None:
        print(f"{incoming_session.id} {incoming_session.title}")
        created: bool = False

        try:
            session: Session = Session.objects.get(external_id=incoming_session.id)
            session.name = incoming_session.title
            session.description = incoming_session.description
            session.scheduled_at = incoming_session.startsAt
            session.duration = incoming_session.duration
            session.title = incoming_session.title
            session.room = room
        except Session.DoesNotExist:
            session: Session = Session(
                external_id=incoming_session.id,
                name=incoming_session.title,
                description=incoming_session.description,
                scheduled_at=incoming_session.startsAt,
                duration=incoming_session.duration,
                title=incoming_session.title,
                room=room,
            )
            created = True

            parent_page.add_child(instance=session)

        speakers = Speaker.objects.filter(external_id__in=incoming_session.speakers)
        for speaker in speakers:
            session.speakers.add(speaker)

        session.save()
        session.save_revision().publish()
        print(
            f'{incoming_session.id} {incoming_session.title} {created and "CREATED" or "UPDATED"}'
        )

    def save_room(self, incoming_room: RoomModel) -> Room:
        room, created = Room.objects.get_or_create(name=incoming_room.name)
        return room
