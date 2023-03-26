from django.contrib.gis.db import models


# Create your models here.
class myPolygon(models.Model):
   geom = models.PolygonField()

# Create your models here.

class supervisor(models.Model):
    nom=models.CharField(max_length=100,null=True)
    prenom=models.CharField(max_length=100,null=True)
    NB_GSM=models.CharField(max_length=100,null=True)
    pseudo=models.CharField(max_length=100,null=True)
    e_mail=models.EmailField(max_length=100,null=True)
    position=models.PointField(null=True)
    image=models.ImageField(null=True)
    def __str__(self):
        return f"{self.prenom} {self.nom}"
    

class client(models.Model):
    nom=models.CharField(max_length=100,null=True)
    prenom=models.CharField(max_length=100,null=True)
    NB_GSM=models.CharField(max_length=100,null=True)
    pseudo=models.CharField(max_length=100,null=True)
    e_mail=models.EmailField(max_length=100,null=True)
    position=models.PointField(null=True)
    image=models.ImageField(null=True)
    def __str__(self):
        return f"{self.prenom} {self.nom}"