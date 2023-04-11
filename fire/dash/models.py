
from django.db import models
from django.utils import timezone
import pyowm

#Django model for post object
class Post(models.Model):
    
    temperature = models.BigIntegerField()
    humidity = models.BigIntegerField()
    wind_speed = models.FloatField(null=True)
    created_date = models.DateTimeField(default=timezone.now)

    def get_weather_data(self):
        owm = pyowm.OWM("0f21fa98b6e075b77fd85b3af087e294")
        location = owm.weather_manager().weather_at_place('Bizerte, TN')
        weather = location.weather
        self.wind_speed = weather.wind()['speed']

    def save(self, *args, **kwargs):
        self.get_weather_data()
        super().save(*args, **kwargs)
    

# define how the object should be displayed as a string
    def __str__(self):
        return f'Temperature: {self.temperature}  ___ Humidity: {self.humidity} '