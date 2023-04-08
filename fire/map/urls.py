from django.urls import path
from .views import display_polygone
from . import views

urlpatterns = [

    path('', views.add_project, name='add_project'),
    path('add_client/<int:id>/', views.add_client, name='add_client'),
    path('display_polygone/<int:id>/', views.display_polygone, name='display_polygone'),
    path('display_polygone/<int:id>/add_node', views.add_node, name='addnode'),
    path('display_polygone/<int:id>/all_detail', views.all_node, name='all'),
  
  
]