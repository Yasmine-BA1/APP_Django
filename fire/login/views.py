from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import *
# Create your views here.


def connectas(request):
    return render(request, 'connectas.html', {})

def connectasclient(request):
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
            return redirect('post_list')
        # We pass the form to the template even if it is not valid
        return render(request, 'login.html', {'form': formulaire})
    # We pass the form to the template for GET requests
    return render(request, 'login.html', {'form': LoginForm()})


def connectassupervisor(request):
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
            return redirect('add_project')
        # We pass the form to the template even if it is not valid
        return render(request, 'login.html', {'form': formulaire})
    # We pass the form to the template for GET requests
    return render(request, 'login.html', {'form': LoginForm()})


# def settings(request):
#     return render(request,'settings.html')



