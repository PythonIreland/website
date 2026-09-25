from django.contrib import admin

from sponsors.models import Sponsor, SponsorshipLevel


@admin.register(SponsorshipLevel)
class SponsorshipLevelAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "level",
    )


@admin.register(Sponsor)
class SponsorAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "logo",
    )
