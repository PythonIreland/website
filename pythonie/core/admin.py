from django.contrib import admin

from .models import HomePageSponsorRelationship, SimplePage

admin.site.register(SimplePage)


@admin.register(HomePageSponsorRelationship)
class HomePageSponsorRelationshipAdmin(admin.ModelAdmin):
    list_display = ("homepage", "sponsor", "level")
    list_display_links = None
    list_editable = ("homepage", "sponsor", "level")
    list_filter = ("homepage", "sponsor", "level")
