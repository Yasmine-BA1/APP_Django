from django.urls import path
from .views import stocker_polygone
from . import views

urlpatterns = [

    path('', views.add_project, name='add_project'),
    path('add_client/', views.add_client, name='add_client'),
    path('stocker_polygone/', stocker_polygone, name='stocker_polygone'),
    
]