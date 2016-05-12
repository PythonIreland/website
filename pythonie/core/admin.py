from django.contrib import admin
from core.models import SimplePage
from core.models import HomePageSponsorRelationship

admin.site.register(SimplePage)


@admin.register(HomePageSponsorRelationship)
class HomePageSponsorRelationshipAdmin(admin.ModelAdmin):
    list_display = ('homepage', 'sponsor', 'level')
    list_editable = ('homepage', 'sponsor', 'level')
    list_filter = ('homepage', 'sponsor', 'level')
