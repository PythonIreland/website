from blog.models import BlogPage

from django import template

from wagtail.wagtailcore.models import Site, Page

from meetups.models import Meetup
from sponsors.models import Sponsor

register = template.Library()


@register.inclusion_tag('core/segment.html', takes_context=False)
def show_homepage_segment(homepage_segment):
    return {
        'segment': homepage_segment.segment
    }


@register.inclusion_tag('core/meetup.html', takes_context=True)
def meetups(context):
    self = context.get('self')
    if hasattr(self, 'show_meetups') and self.show_meetups:
        meetups = Meetup.future_events()
    else:
        meetups = []
    return {
        'meetups': meetups,
        'request': context['request'],
    }


@register.inclusion_tag('core/sponsor.html', takes_context=True)
def sponsors(context):
    self = context.get('self')
    if hasattr(self, 'show_sponsors') and self.show_sponsors:
        sponsors = Sponsor.for_event(self)
    else:
        sponsors = []
    return {
        'sponsors': sponsors,
        'request': context['request'],
    }


@register.assignment_tag(takes_context=False)
def root_page():
    site = Site.objects.get(is_default_site=True)
    return Page.objects.page(site.root_page).first()


@register.assignment_tag(takes_context=False)
def child_pages(page):
    pages = page.get_children().live().in_menu().all()
    return pages


@register.assignment_tag(takes_context=False)
def get_blogs(categories, count=3):
    """
    :param categories: Filter by these BlogCategories if specified
    :param count: The number of blogs to limit by
    :return: A queryset of BlogPages
    """
    blog_pages = BlogPage.objects.filter()
    if categories:
        blog_pages = blog_pages.filter(blog_categories__in=categories)
    return blog_pages.order_by('date')[:count]
