from django.shortcuts import render, redirect
from django.contrib.gis.geos import Polygon

from .models import myProject
from django.contrib.gis.geos import GEOSGeometry

from django.http import JsonResponse
from django.contrib.gis.geos import Point
from .forms import *

def add_project(request):
    projects = myProject.objects.all()
    # project = myProject.objects.get(polygon_id=id)

    clients = client.objects.all()
    if request.method == 'POST':

        formulairep = Form_project(request.POST)
        # Get the other data from the form data
        nomp = request.POST.get('nomp')
        descp = request.POST.get('descp')
        debutp = request.POST.get('debutp')
        finp = request.POST.get('finp')
        cityp = request.POST.get('cityp')
        # clientp = request.POST.get('clientp')

        if formulairep.is_valid():
            # Get the selected client from the form
            selected_client_id = request.POST.get('clientp')

            # Get the client object based on the selected ID
            selected_client = client.objects.get(id=selected_client_id)
                 
            formulairep.enregistrerProj()
            polygonString = request.POST.get('points')
            print(polygonString)
            polygon = GEOSGeometry(polygonString, srid=4326)
            instance = myProject(nomp=nomp,descp=descp,debutp=debutp,finp=finp,cityp=cityp,geomp=polygon,clientp=selected_client)
            instance.save()
                    
            return redirect('add_client',id=instance.polygon_id)
        return render(request, 'addproj.html', {'form': formulairep,'projects':projects})
    return render(request, 'addproj.html', {'form': Form_project(),'projects':projects})


def add_client(request,id):
        project = myProject.objects.get(polygon_id=id)
        
        if request.method == 'POST':
            formulaire = Form_client(request.POST)
            if formulaire.is_valid():
                formulaire.enregistrer()
                pseudo = formulaire.cleaned_data['pseudo']
                variable = 'client'

                return redirect('display_polygone',id)
            return render(request, 'addclient.html', {'form': formulaire,'project':project})
        return render(request, 'addclient.html', {'form': Form_client(),'project':project})

        

def display_polygone(request,id):
    projects = myProject.objects.all()
    project = myProject.objects.get(polygon_id=id)

    if request.method == 'POST':
        # id=instance.polygon_id

       
        return redirect('addnode',id)
    return render(request, 'displaypoly.html', {'projects':projects,'project':project})


def add_node(request, id):
    projects = myProject.objects.all()
    project = myProject.objects.get(polygon_id=id)

    if request.method == 'POST':
        node_name = request.POST.get('nom') 
        mylatitude = request.POST.get('latitude') 
        mylongitude = request.POST.get('longitude') 
        point=Point(x=float(mylongitude),y=float(mylatitude))
        project_id = request.POST.get('polyg')
        project_instance = myProject.objects.get(polygon_id=project_id)

        instance = node(position=point,nom=node_name, polyg=project_instance, latitude=mylatitude, longitude=mylongitude)
        instance.save()

        return redirect('all',id)

    return render(request, 'add_node.html', { 'projects': projects, 'project': project})


def all_node(request,id):
    projects = myProject.objects.all()
    project = myProject.objects.get(polygon_id=id)

    marker = node.objects.all()
    nodeq = node.objects.filter(polyg=project)
    print('****',nodeq)
    
    for node_instance in nodeq:
        # get the latitude and longitude values from the node instance
        latitude = node_instance.latitude
        longitude = node_instance.longitude
        position=node_instance.position
        nom=node_instance.nom
        
        print('nom:',nom)
        print('x:',node_instance.position.x)
        print('y:',node_instance.position.y)
        print('position:',position)
        
    #no = node.objects.order_by('-id').first()
    #bla = no.nom
    #print(bla)

    return render(request, 'all.html', { 'node_instance': node_instance,'nodee': nodeq,'markers': marker,'projects':projects, 'project': project})




def ALL(request,id):
    projects = myProject.objects.all()
    project = myProject.objects.get(polygon_id=id)

    marker = node.objects.all()
    nodeq = node.objects.filter(polyg=project)
    
    
    for node_instance in nodeq:
        # get the latitude and longitude values from the node instance
        latitude = node_instance.latitude
        longitude = node_instance.longitude
        position=node_instance.position
        nom=node_instance.nom
        print('nom:',nom)
        print('position:',position)

    return render(request, 'ALL_node.html', {  'node_instance': node_instance,'node': nodeq,'markers': marker,'projects':projects, 'project': project})


def interface_c(request):
    projects = myProject.objects.all()
   

    marker = node.objects.all()
   
    
    
    return render(request, 'interface_c.html',{'markers': marker,'projects':projects})
