from django.shortcuts import render, redirect
from django.contrib.gis.geos import Polygon

from .models import myProject
from django.contrib.gis.geos import GEOSGeometry

from django.http import JsonResponse
from django.contrib.gis.geos import Point
from .forms import *

def add_project(request):
    projects = myProject.objects.all()
    if request.method == 'POST':

        formulairep = Form_project(request.POST)
        if formulairep.is_valid():
                 
            formulairep.enregistrerProj()
                
            return redirect('add_client')
        return render(request, 'addproj.html', {'form': formulairep,'projects':projects})
    return render(request, 'addproj.html', {'form': Form_project(),'projects':projects})


def add_client(request):
        
        if request.method == 'POST':
            formulaire = Form_client(request.POST)
            if formulaire.is_valid():
                formulaire.enregistrer()
                pseudo = formulaire.cleaned_data['pseudo']
                variable = 'client'

                return redirect('stocker_polygone')
            return render(request, 'addclient.html', {'form': formulaire})
        return render(request, 'addclient.html', {'form': Form_client()})

        

def stocker_polygone(request):
    if request.method == 'POST':
        polygonString = request.POST.get('points')
        print(polygonString)
        polygon = GEOSGeometry(polygonString, srid=4326)
        instance = myProject(geomp=polygon)
        instance.save()
       
        return redirect('home')
    return render(request, 'map.html')
