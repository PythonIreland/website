from django import template

register = template.Library()


@register.inclusion_tag('core/segment.html', takes_context=False)
def show_homepage_segment(homepage_segment):
    return {
        'segment': homepage_segment.segment
    }

@register.inclusion_tag('core/meetup.html', takes_context=False)
def show_meetup(meetup):
    return {
        'meetup': meetup
    }
