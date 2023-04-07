from django.shortcuts import render, redirect
from django.contrib.auth import authenticate , login 
from .models import *

from signup.models import supervisor
from signup.models import client
# from map.models import mPolygons

from django.core.serializers import serialize
from django.http import JsonResponse
from django.contrib.gis.geos import GEOSGeometry

def home(request):
    return render(request, 'home.html')

def index(request):
    return render(request,'index.html')

def dashboard(request):
    return render(request,'index/dashboard.html')

def markers(request):
    # mymap= myPolygon.objects.all()
    return render(request,'index/markers.html')



def profile(request):
    mysupervisor= supervisor.objects.all()
    myclient= client.objects.all()
    return render(request,'index/profile.html',{'sup':mysupervisor,'cli':myclient})

def settings(request):
    return render(request,'index/settings.html')




    