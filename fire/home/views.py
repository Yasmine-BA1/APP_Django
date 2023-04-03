from django.shortcuts import render, redirect
from django.contrib.auth import authenticate , login 
from .models import *
from .forms import *
from signup.models import supervisor
from signup.models import client
from map.models import myPolygon


def home(request):
    return render(request, 'home.html')

def index(request):
    return render(request,'index.html')

def dashboard(request):
    return render(request,'dashboard.html')

def markers(request):
    mymap= myPolygon.objects.all()
    return render(request,'markers.html',{'map':mymap})

def profile(request):
    mysupervisor= supervisor.objects.all()
    myclient= client.objects.all()
    return render(request,'profile.html',{'sup':mysupervisor,'cli':myclient})

def settings(request):
    return render(request,'settings.html')


def connect(request):
    if request.method == 'POST':
        formulaire = LoginForm(request.POST)
        if formulaire.is_valid(request):
            pseudo = formulaire.cleaned_data['pseudo']
            mot_de_passe = formulaire.cleaned_data['mot_de_passe']
            data = authenticate(request, username=pseudo,
                                password=mot_de_passe)
            if data is not None:
                login(request, data)
                #### on va redirect dashboard #####
                # return redirect('map/')
            return redirect('dash/')
        # We pass the form to the template even if it is not valid
        return render(request, 'login.html', {'form': formulaire})
    # We pass the form to the template for GET requests
    return render(request, 'login.html', {'form': LoginForm()})


    