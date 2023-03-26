# from django.contrib.gis import admin
# from .models import myPolygon

# from django.contrib import admin
# from .models import Post

# admin.site.register(Post)

# # Register your models here.

# admin.site.register(myPolygon)
# class polygonAdmin(admin.GISModelAdmin):
#     list_display = ("geom")

from django.contrib import admin
#from .models import test

from django.contrib.gis import admin
from .models import myPolygon


#admin.site.register(test)

admin.site.register(myPolygon)
class polygonAdmin(admin.GISModelAdmin):
    list_display = ("geom")