
from django.db import models
from django.utils import timezone


#Django model for post object
class Post(models.Model):
    
    temperature = models.BigIntegerField()
    humidity = models.BigIntegerField()
    
    created_date = models.DateTimeField(default=timezone.now)
    

# define how the object should be displayed as a string
    def __str__(self):
        return f'Temperature: {self.temperature}  ___ Humidity: {self.humidity} ___ created: {self.created_date}'