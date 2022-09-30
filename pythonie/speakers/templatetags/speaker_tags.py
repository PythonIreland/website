from django import template

register = template.Library()


@register.inclusion_tag('speakers/speaker_picture.html')
def speaker_picture(speaker):
    return {'url': speaker.picture_url, 'name': speaker.name}
