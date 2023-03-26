from django.shortcuts import render, redirect
from .models import myPolygon
from django.contrib.gis.geos import GEOSGeometry

# Create your views here.
def stocker_polygone(request):
    if request.method == 'POST':
        polygonString = request.POST.get('points')
        print(polygonString)
        polygon = GEOSGeometry(polygonString, srid=4326)
        instance = myPolygon(geom=polygon)
        instance.save()
       
        return redirect('stocker_polygone')
    return render(request, 'map.html')
