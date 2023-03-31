# from django.contrib.gis.db import models

# # Create your models here.
# class myPolygon(models.Model):
   
#     geom = models.PolygonField()


from django.conf import settings
from django.db import models
from django.utils import timezone

############polyg##########
from django.contrib.gis.db import models
from signup.models import client
from signup.models import supervisor

    

class myPolygon(models.Model):
    nom = models.CharField(max_length=50, null=True)
    geom = models.PolygonField()

    client = models.ForeignKey(client, on_delete=models.CASCADE, null=True, related_name='%(class)s_related')
    supervisor = models.ForeignKey(supervisor, on_delete=models.CASCADE, null=True, related_name='%(class)s_related')


    def __str__(self):
        return f'map : Project: {self.nom}  ---  client: {self.client}  ---  supervisor: {self.supervisor}'