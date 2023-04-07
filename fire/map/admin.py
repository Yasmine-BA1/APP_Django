from django.contrib import admin
from django.contrib.gis import admin
# from .models import mPolygons
from .models import myProject



# admin.site.register(mPolygons)
admin.site.register(myProject)
class polygonAdmin(admin.GISModelAdmin):
    list_display = ("geom")