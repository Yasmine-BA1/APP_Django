from django.shortcuts import render, redirect
from django.contrib.gis.geos import Polygon

from .models import myProject
from dash.models import Post
from signup.models import supervisor
from django.contrib.gis.geos import GEOSGeometry


from django.http import JsonResponse
from django.contrib.gis.geos import Point
from .forms import *
import pyowm 
import PyFWI

def add_project(request,pseudo):
    projects = myProject.objects.all()
    supervisors = supervisor.objects.get(pseudo=pseudo)
    
    # supervisorp = request.POST.get('supervisors')
    print("++++++supervisorp", supervisors)

    clients = client.objects.all()
    if request.method == 'POST':


        formulairep = Form_project(request.POST)
        # Get the other data from the form data
        nomp = request.POST.get('nomp')
        descp = request.POST.get('descp')
        debutp = request.POST.get('debutp')
        finp = request.POST.get('finp')
        cityp = request.POST.get('cityp')


        if formulairep.is_valid():
            # Get the selected client from the form
            selected_client_id = request.POST.get('clientp')

            # Get the client object based on the selected ID
            selected_client = client.objects.get(id=selected_client_id)
                 
            formulairep.enregistrerProj()

            multiPolygone= request.POST.get('points')
            print(multiPolygone)
            polygon = GEOSGeometry(multiPolygone, srid=4326)

            instance = myProject(nomp=nomp,descp=descp,debutp=debutp,finp=finp,cityp=cityp,geomp=polygon,clientp=selected_client,supervisorp=supervisors)
            instance.save()
                    
            # return redirect('add_client',id=instance.polygon_id)
            return redirect('display_polygone',pseudo=pseudo,id=instance.polygon_id)
        return render(request, 'addproj.html', {'form': formulairep,'projects':projects,'supervisor':supervisors})
    return render(request, 'addproj.html', {'form': Form_project(),'projects':projects,'supervisor':supervisors})


def add_client(request,pseudo):
        # project = myProject.objects.get(polygon_id=id)
        supervisors = supervisor.objects.get(pseudo=pseudo)
        if request.method == 'POST':
            formulaire = Form_client(request.POST)
            if formulaire.is_valid():
                formulaire.enregistrer()
                pseudo = formulaire.cleaned_data['pseudo']
                variable = 'client'

                
                return redirect('add_project')
            return render(request, 'addclient.html', {'form': formulaire,'supervisor':supervisors})
        return render(request, 'addclient.html', {'form': Form_client(),'supervisor':supervisors})


def display(request,pseudo):
    # projects = myProject.objects.all()
    # supervisors = supervisor.objects.get(pseudo=pseudo)
    
    supervisor_obj = supervisor.objects.get(pseudo=pseudo)
    projects = myProject.objects.filter(supervisorp=supervisor_obj)
    print("/////////", supervisor_obj.pseudo)
    print("/////projects////",projects )

    for proj in projects :
        print("/////proj////", proj)

    return render(request, 'display.html', {'projects':projects,'supervisor_obj':supervisor_obj})


def display_polygone(request,id,pseudo):
    supervisor_obj = supervisor.objects.get(pseudo=pseudo)
    print("//supervisor_obj/", supervisor_obj)
    projects = myProject.objects.filter(supervisorp=supervisor_obj)
    project = myProject.objects.get(polygon_id=id)
    print("//project/", project.supervisorp)

    if request.method == 'POST':
        # id=instance.polygon_id

       
        return redirect('addnode',pseudo,id)
    return render(request, 'displaypoly.html', {'projects':projects,'project':project,'supervisor_obj':supervisor_obj})


def add_node(request, id,pseudo):
    supervisor_obj = supervisor.objects.get(pseudo=pseudo)
    projects = myProject.objects.filter(supervisorp=supervisor_obj)
    project = myProject.objects.get(polygon_id=id)

    marker = node.objects.all()
    nodeq = node.objects.filter(polyg=project)
    
    

    if request.method == 'POST':
        node_name = request.POST.get('nom') 
        mylatitude = request.POST.get('latitude') 
        mylongitude = request.POST.get('longitude') 
        point=Point(x=float(mylongitude),y=float(mylatitude))
        project_id = request.POST.get('polyg')
        project_instance = myProject.objects.get(polygon_id=project_id)

        instance = node(position=point,nom=node_name, polyg=project_instance, latitude=mylatitude, longitude=mylongitude)
        instance.save()

        return redirect('all',pseudo,id)

    return render(request, 'add_node.html', { 'projects': projects, 'project': project,'nodee':nodeq})


def all_node(request,id,pseudo):
    posts = Post.objects.all()
    for post_instance in posts:
        print('***wind',post_instance.wind_speed)

    supervisor_obj = supervisor.objects.get(pseudo=pseudo)
    projects = myProject.objects.filter(supervisorp=supervisor_obj)
    project = myProject.objects.get(polygon_id=id)

    marker = node.objects.all()
    nodeq = node.objects.filter(polyg=project)
    print('****nodeq:',nodeq)
    l=len(nodeq)
    print('****nodeq length:', len(nodeq))
    
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
    
    if request.method == 'POST':
        return redirect('addnode',pseudo,id)
        
    #no = node.objects.order_by('-id').first()
    #bla = no.nom
    #print(bla)
    context = { 'l':l,'projects':projects,'project':project,'node_instance': node_instance,'nodee': nodeq,'markers': marker,'post_instance':post_instance}
    return render(request, 'all.html',context)

def modify(request,id,pseudo):
    posts = Post.objects.all()
    for post_instance in posts:
        print('***wind',post_instance.wind_speed)

    supervisor_obj = supervisor.objects.get(pseudo=pseudo)
    projects = myProject.objects.filter(supervisorp=supervisor_obj)
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

    
    if request.method == 'POST':
        return redirect('addnode',pseudo,id)

    context = {'projects':projects,'project':project,'nodee': nodeq,'markers': marker,'post_instance':post_instance}
    return render(request, 'modify.html',context)





def ALL(request,id,pseudo):


    posts = Post.objects.all()
    for post_instance in posts:
        print('***wind',post_instance.wind_speed)

    supervisor_obj = supervisor.objects.get(pseudo=pseudo)
    projects = myProject.objects.filter(supervisorp=supervisor_obj)
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

    return render(request, 'ALL_node.html', { 'node_instance': node_instance,'nodee': nodeq,'markers': marker,'projects':projects, 'project': project,'post_instance':post_instance})



def interface_c(request, pseudo):
    posts = Post.objects.all()
    for post_instance in posts:
        print('***wind',post_instance.wind_speed)

    clientp = client.objects.get(pseudo=pseudo)
    print('nom client',clientp.nom)
    print('---------image url client',clientp.image.url)
    projects = myProject.objects.filter(clientp=clientp)
    # print('***',projects)
    for proj_instance in projects:
        print('namep',proj_instance.nomp)
        # print('geomp',proj_instance.geomp)
    
    

    nodeq = node.objects.filter(polyg=proj_instance)
    for node_instance in nodeq:
        # get the latitude and longitude values from the node instance
        latitude = node_instance.latitude
        longitude = node_instance.longitude
        position=node_instance.position
        nom=node_instance.nom
        print('---node name:',nom)
        # print('---node position:',position)

    context = {'nodee':nodeq,'clientp':clientp,'projects': projects, 'pseudo': pseudo,'proj_instance':proj_instance,'node_instance':node_instance,'post_instance':post_instance}
    return render(request, 'interface_c.html', context)

   
    
    
    
