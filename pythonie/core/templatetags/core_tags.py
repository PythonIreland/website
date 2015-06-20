from django import template
from wagtail.wagtailcore.models import Site
from core.models import HomePage

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

@register.assignment_tag(takes_context=False)
def root_page():
    site = Site.objects.get(is_default_site=True)
    return HomePage.objects.page(site.root_page).first()
