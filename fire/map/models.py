from django.db import models
from django.contrib.gis.db import models

# Create your models here.
class myPolygon(models.Model):
   geom = models.PolygonField()