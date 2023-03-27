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



# class test(models.Model):
#     author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     title = models.CharField(max_length=200)
#     text = models.TextField()
#     created_date = models.DateTimeField(default=timezone.now)
#     published_date = models.DateTimeField(blank=True, null=True)

#     def publish(self):
#         self.published_date = timezone.now()
#         self.save()

#     def __str__(self):
#         return self.title
    

class myPolygon(models.Model):
    nom = models.CharField(max_length=50, null=True)
    geom = models.PolygonField()

    client = models.ForeignKey(client, on_delete=models.CASCADE, null=True, related_name='%(class)s_related')
    supervisor = models.ForeignKey(supervisor, on_delete=models.CASCADE, null=True, related_name='%(class)s_related')