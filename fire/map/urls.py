from django.urls import path
from .views import display_polygone
from . import views

urlpatterns = [

    
    path('sup_<str:pseudo>', views.add_client, name='add_client'),
    path('sup_<str:pseudo>/add_project/', views.add_project, name='add_project'),
    path('sup_<str:pseudo>/Projects_List/', views.display, name='display'),
    path('sup_<str:pseudo>/display_polygone/<int:id>/', views.display_polygone, name='display_polygone'),
    path('sup_<str:pseudo>/display_polygone/<int:id>/add_node', views.add_node, name='addnode'),
    path('sup_<str:pseudo>/display_polygone/<int:id>/all_detail', views.all_node, name='all'),
    path('sup_<str:pseudo>/display_polygone/<int:id>/modify', views.modify, name='modify'),
    path('sup_<str:pseudo>/display_polygone/<int:id>/nodes', views.ALL, name='ALL_node'),
    
    path('update/<int:id>/', views.start_mqtt, name='update'),
  
    path('interface/<str:pseudo>', views.interface_c, name='interface_c'),
  
    path('update_weather/<int:id>/', views.update_weather, name='update_weather'),
   
]