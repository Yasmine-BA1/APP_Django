from django.shortcuts import render, redirect
from .forms import *
#from .models import myPolygon
#from django.contrib.gis.geos import GEOSGeometry

# Create your views here.
def compte(request, pk):
    if pk == 'supervisor':
        if request.method == 'POST':
            formulaire = Form_supervisor(request.POST)
            if formulaire.is_valid():
                formulaire.enregistrer()
                pseudo = formulaire.cleaned_data['pseudo']
                variable = 'supervisor'
                return redirect('map', variable, pseudo)
            return render(request, 'signup.html', {'form': formulaire})
        return render(request, 'signup.html', {'form': Form_supervisor()})
    else:
        if request.method == 'POST':
            formulaire = Form_client(request.POST)
            if formulaire.is_valid():
                formulaire.enregistrer()
                pseudo = formulaire.cleaned_data['pseudo']
                variable = 'client'
                return redirect('map', variable, pseudo)
            return render(request, 'signup.html', {'form': formulaire})
        return render(request, 'signup.html', {'form': Form_client()})
    


# def maps(request, variable, pseudo):
#     if request.method == 'POST':
#         formulaire = position(request.POST)
#         if formulaire.is_valid():
#             if variable == 'composteur':
#                 formulaire.enregistrer_composteur(pseudo)
#             else:
#                 formulaire.enregistrer_greener(pseudo)
#         return render(request, 'page1/map.html', {'form': formulaire})
#     return render(request, 'page1/map.html', {'form': position()})


# def stocker_polygone(request):
#     if request.method == 'POST':
#         polygonString = request.POST.get('points')
#         print(polygonString)
#         polygon = GEOSGeometry(polygonString, srid=4326)
#         instance = myPolygon(geom=polygon)
#         instance.save()
       
#         return redirect('stocker_polygone')
#     return render(request, 'map.html')