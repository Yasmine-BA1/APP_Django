from django.contrib.gis import admin
#from .models import myPolygon

from.models import *
# Register your models here.

admin.site.register(client)
admin.site.register(supervisor)




# Register your models here.


# Register your models here.
# admin.site.register(myPolygon)
# class polygonAdmin(admin.GISModelAdmin):
#     list_display = ("geom")
