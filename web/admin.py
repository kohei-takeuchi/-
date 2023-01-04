from django.contrib.gis import admin

from .models import depthdata,purchasedata,correctdata,lightdata,bufferdata


@admin.register(depthdata)
class WebAdmin(admin.OSMGeoAdmin):
    """Marker admin."""

    list_display = ('計測時刻',)
@admin.register(purchasedata)
class PurchaseAdmin(admin.OSMGeoAdmin):
    """Marker admin."""

    list_display = ('ID',)
@admin.register(lightdata)
class LightAdmin(admin.OSMGeoAdmin):
    """Marker admin."""
    list_display = ('緯度',)
@admin.register(correctdata)
class CorrectAdmin(admin.OSMGeoAdmin):
    """Marker admin."""

    list_display = ('最終変更時刻',)
@admin.register(bufferdata)
class BufferAdmin(admin.OSMGeoAdmin):
    """Marker admin."""

    list_display = ('投稿時刻',)
