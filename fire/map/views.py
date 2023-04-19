from django.shortcuts import render, redirect
from django.contrib.gis.geos import Polygon
import json
from multiprocessing.connection import Client
from statistics import geometric_mean
from unittest import result
from .models import myProject

from signup.models import supervisor
from django.contrib.gis.geos import GEOSGeometry


from django.http import JsonResponse
from django.contrib.gis.geos import Point
from .forms import *
import pyowm 
from .mqtt import start_mqtt_client
from .status import result
import csv 
from .FWI import *
from datetime import datetime


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
#-----------------------------------------------------------------------------

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
        Sensors = request.POST.get('Sensors') 
        reference = request.POST.get('reference') 
        range_str = request.POST.get('range')
        node_range = int(range_str) 
        mylatitude = request.POST.get('latitude') 
        mylongitude = request.POST.get('longitude') 
        point=Point(x=float(mylongitude),y=float(mylatitude))
        project_id = request.POST.get('polyg')
        project_instance = myProject.objects.get(polygon_id=project_id)

        instance = node(position=point,nom=node_name, polyg=project_instance, latitude=mylatitude, longitude=mylongitude,reference=reference,node_range=node_range,Sensors=Sensors)
        instance.save()

        new_data = Data(temperature=0, humidity=0, wind=0, node=instance)
        new_data.save()

        datas = Data.objects.filter(node=instance)
        print('hello')
        print(instance.nom)
        print(datas)
    

        return redirect('all',pseudo,id)

    return render(request, 'add_node.html', { 'projects': projects, 'project': project,'nodee':nodeq})
#--------------------------------------------------------------------

def start_mqtt(request,id):
    # Start the MQTT client
    start_mqtt_client(id)
    
    # Return a simple response to indicate that the client has started
    #return HttpResponse('MQTT client started successfully.')
    return render(request, 'all.html', {})



def all_node(request,id,pseudo):
    supervisor_obj = supervisor.objects.get(pseudo=pseudo)
    projects = myProject.objects.filter(supervisorp=supervisor_obj)
    my_project = myProject.objects.get(polygon_id=id)

    nodes = node.objects.filter(polyg=my_project).order_by('-Idnode')
    # print('****nodes:',nodes)
    onode = nodes[0] # =======node_instance// last one
    print('last node added',onode) 

    datas = Data.objects.filter(node=onode).order_by('-IdData')
    data = datas.first()
    # print('dataaaaaa',data)

    temperature = data.temperature
    humidity = data.humidity
    wind_speed = data.wind
    rain_volume =data.rain
    

    with open('testBatch.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([datetime.today().strftime('%m/%d/%Y'), temperature, humidity, wind_speed,rain_volume,'0'])
        


    batchFWI('testBatch.csv')
    
   
    with open('testBatch.csv', mode='r') as file:
        reader = csv.reader(file)
        rows = list(reader)
        last_row = rows[-1]
        FWI = last_row[-1]
    
    
    # fwi = float(FWI)
    # onode.FWI=fwi
    # onode.save()
    # print('ffffffffffwi',fwi)
    
    data_list = []
    for n in nodes :
        ds = Data.objects.filter(node=n).order_by('-IdData').first()
        data_list.append(
            ds,
        )
        
    
    print('data liiiiiiist',data_list)
    
    for i in range(len(data_list)):
        ldn0 = data_list[i]
        #node = ldn0.node
        print(ldn0)
        dd = ldn0.wind
        print(dd)
        
        # fwi = float(FWI)
        # ldn0.node.FWI=fwi
        # ldn0.node.save()
        # print('ffffffffffwi',fwi)
        
        
        # status = result(id)
        # ldn0.node.status = status
        # ldn0.node.save()
        # print('sssssssss',status)
        # print('-----------------------------')
    

    print('-----------------------------')
    my_project = myProject.objects.get(polygon_id=id)

    status = result(id)
   

    nodes = node.objects.filter(polyg=my_project).order_by('-Idnode')
    onode = nodes[0]
    
    fwi = float(FWI)
    onode.FWI=fwi
    onode.save()
    print('ffffffffffwi',fwi)

    onode.status = status
    onode.save()
    print('last    sssssssss',status)


    # print('temperature',temperature)


    
    for node_instance in nodes:
        nom=node_instance.nom       
        # print('nom:',nom)
    

    
    

    
    if request.method == 'POST':
        return redirect('addnode',pseudo,id)
        

    context = { 'projects':projects,'project':my_project,'node_instance': node_instance,'nodee': nodes,'node':onode,'parm':data, 'ldn':data_list}
    return render(request, 'all.html',context)

# def update_weather(request, id):
#     # get updated weather information
#     my_project = myProject.objects.get(polygon_id=id)

#     status = result(id)
   

#     nodes = node.objects.filter(polyg=my_project).order_by('-Idnode')
#     onode = nodes[0]

#     onode.status = status
#     onode.save()
#     # print('statussssss',status)


#     # status = node.status
#     # fwi = node.FWI
#     # rssi= node.RSSI
    
#     status =onode.status
#     fwi=onode.FWI
#     rssi=onode.RSSI
#     node_name =onode.nom
#     # print('oonodeee',status)

#     datas = Data.objects.filter(node=onode).order_by('-IdData')
#     # print("ddddddddddd",datas)
#     data = datas.first()
    

#     data = {
#         'temperature': data.temperature,
#         'humidity': data.humidity,
#         'wind': data.wind,
#         'rain': data.rain,
#         'RSSI' : rssi,
#         # # 'camera' : cam,
#         'fwi' : fwi,
#         'status' : status,
#         'node':node_name,
#         }
#     # print('fffff',data['fwi'])
#     # print('fffff',data['RSSI'])
#     # print('fffff',data['status'])
#     # # get node status, fwi, and rssi
#     # node_status = onode.status
#     # node_fwi = onode.FWI
#     # node_rssi = onode.RSSI
#     # node_name =onode.nom
#     # # add node status, fwi, and rssi to data
#     # data['status'] = node_status
#     # data['fwi'] = node_fwi
#     # data['RSSI'] = node_rssi
#     # data['node'] = node_name
#     # print("oooooooo",data)
    

#     # return a JsonResponse with the updated data
#     return JsonResponse(data)
#     # return JsonResponse({"datas": list(datas.values())})


def modify(request,id,pseudo):
    posts = Data.objects.all()
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
    supervisor_obj = supervisor.objects.get(pseudo=pseudo)
    projects = myProject.objects.filter(supervisorp=supervisor_obj)
    project = myProject.objects.get(polygon_id=id)

    nodes = node.objects.filter(polyg=project).order_by('-Idnode')
    # print('****nodes:',nodes)
    onode = nodes[0] # =======node_instance// onlyy for the last one
    # print(onode) 

    datas = Data.objects.filter(node=onode).order_by('-IdData')
    data = datas.first()


    nodeq = node.objects.filter(polyg=project)
    nodes_data = []
    for node_instance in nodeq:
        datas = Data.objects.filter(node=node_instance).order_by('-IdData')
        data = datas.first()
        nodes_data.append({'node_instance': node_instance, 'data': data})
        
    data_list = []
    for n in nodes :
        ds = Data.objects.filter(node=n).order_by('-IdData').first()
        data_list.append(
            ds,
        )
        

    print('data liiiiiiist',data_list)
    
    for i in range(len(data_list)):
        ldn0 = data_list[i]
        #node = ldn0.node
        print(ldn0)
        dd = ldn0.wind
        print(dd)

        temperature = ldn0.temperature
        humidity = ldn0.humidity
        wind_speed = ldn0.wind
        
    # print('------nodes_data',nodes_data)
    context = {'nodes_data': nodes_data,'nodee': nodeq,'node':onode,'projects':projects, 'project': project,'parm':data,'ldn':data_list}
   

    return render(request, 'ALL_node.html',context )



def interface_c(request, pseudo):
    datas = Data.objects.all()
    for post_instance in datas:
        print('***wind',post_instance.wind)

    clientp = client.objects.get(pseudo=pseudo)
    # print('nom client',clientp.nom)
    # print('---------image url client',clientp.image.url)
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
        # print('---node name:',nom)
        # print('---node position:',position)

    nodes_data = []
    for node_instance in nodeq:
        datas = Data.objects.filter(node=node_instance).order_by('-IdData')
        data = datas.first()
        nodes_data.append({'node_instance': node_instance, 'data': data})

    context = {'nodes_data': nodes_data,'nodee':nodeq,'clientp':clientp,'projects': projects, 'pseudo': pseudo,'proj_instance':proj_instance,'node_instance':node_instance,'post_instance':post_instance}
    return render(request, 'interface_c.html', context)

   
    
    
    
