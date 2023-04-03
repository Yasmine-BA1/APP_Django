from django.contrib import admin
from django.urls import path,include
from django.conf import settings 
from django.conf.urls.static import static
from home import views

urlpatterns = [
    path('', views.home,name='home' ),
    path('index/', views.index,name='index' ),
    path('dashboard/', views.dashboard, name='dashboard' ),
    path('markers/', views.markers, name='markers' ),
    path('profile/', views.profile, name='profile' ),
    path('settings/', views.settings, name='settings' ),

    path('connect/',views.connect,name='connect')



]