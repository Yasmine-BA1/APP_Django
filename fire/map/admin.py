from django.contrib.gis import admin

# Register your models here.

from .models import myPolygon
# Register your models here.
admin.site.register(myPolygon)
class polygonAdmin(admin.GISModelAdmin):
    list_display = ("geom")
