from django.contrib import admin
from sponsors.models import Sponsor


class SponsorAdmin(admin.ModelAdmin):
    list_display = ('name', 'logo',)

admin.site.register(Sponsor, SponsorAdmin)

