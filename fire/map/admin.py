from django.contrib import admin
from django.contrib.gis import admin
from .models import myPolygon




admin.site.register(myPolygon)
class polygonAdmin(admin.GISModelAdmin):
    list_display = ("geom")