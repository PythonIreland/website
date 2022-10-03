from django import template
from speakers.models import Speaker

register = template.Library()


@register.inclusion_tag('speakers/speaker_picture.html')
def speaker_picture(speaker: Speaker, size: int = 75):
    picture_url = speaker.picture_url
    if not picture_url:
        picture_url = f'https://robohash.org/{speaker.name}'
    return {'url': picture_url, 'name': speaker.name, 'size': size}
