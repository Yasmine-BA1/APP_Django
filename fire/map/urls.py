from django.urls import path
from .views import display_polygone
from . import views

urlpatterns = [

    path('', views.add_project, name='add_project'),
    path('add_client/', views.add_client, name='add_client'),
    path('display_polygone/', views.display_polygone, name='display_polygone'),
    
]