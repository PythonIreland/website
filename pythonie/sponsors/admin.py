from django.contrib import admin
from sponsors.models import Sponsor, SponsorshipLevel


class SponsorshipLevelAdmin(admin.ModelAdmin):
    list_display = ('name', 'level',)

admin.site.register(SponsorshipLevel, SponsorshipLevelAdmin)


class SponsorAdmin(admin.ModelAdmin):
    list_display = ('name', 'logo',)

admin.site.register(Sponsor, SponsorAdmin)
