from django.contrib.gis import admin

from .models import Account


@admin.register(Account)
class AccountAdmin(admin.OSMGeoAdmin):
    """Marker admin."""

    list_display = ('uuid',)
# Register your models here.
