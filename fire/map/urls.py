from django.urls import path
from .views import stocker_polygone
from . import views

urlpatterns = [
    path('', stocker_polygone, name='stocker_polygone'),
    path('stocker_polygone/', stocker_polygone, name='stocker_polygone'),
    #path('', views.stocker_polygone, name='stocker_polygone'),
    
]