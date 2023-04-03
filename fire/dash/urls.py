from django.urls import path,include
from . import views

urlpatterns=[
    path('', views.post_list, name='post_list'),
    path('UPdate', views.start_mqtt, name='update'),

    path('getTemp',views.getTemp,name='getTemp'),

]