from django.urls import path
from .views import stocker_polygone
from . import views 

urlpatterns = [
     path('map/', views.stocker_polygone, name='stocker_polygone'),


]
