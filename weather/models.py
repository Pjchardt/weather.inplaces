import os
import requests
from geopy.geocoders import Nominatim

from django.db import models

DARKSKYURL = "https://api.darksky.net/forecast/"
if 'DARKSKY_KEY' not in os.environ:
    from django.conf import settings
    import json
    with open("{0}\\{1}".format(settings.BASE_DIR, 'django_config.json')) as f:
        config = json.load(f)
    DSKEY = config['darksky_key']
else:
    DSKEY = os.environ['DARKSKY_KEY']

# Create your models here.
class User(models.Model):
    user_name = models.CharField(max_length=64)
    def __str__(self):
        return self.user_name

class LocationWeather(models.Model):
    parent = models.ForeignKey('User', related_name='child_set', null=True, on_delete=models.CASCADE)
    location_querry = models.CharField(max_length=128)
    location = models.CharField(max_length=128, default='none')
    lat = models.FloatField(default=1.0)
    long = models.FloatField(default=1.0)
    weather_summary = models.CharField(max_length=128, default='none')
    weather_temperature = models.CharField(max_length=128, default='none')
    def __str__(self):
        return self.location
    def get_weather(self):
        geolocator = Nominatim(user_agent="weather.somewhere")
        location = geolocator.geocode(self.location_querry)
        if location is None:
            return False
        self.location = location.address
        self.lat = location.latitude
        self.long = location.longitude
        full_url = "{0}{1}/{2},{3}".format(DARKSKYURL, DSKEY, self.lat, self.long)
        PARAMS = {'exclude': 'minutely,hourly,daily,alerts,flags'}
        r = requests.get(url = full_url, params = PARAMS)
        data = r.json()
        self.weather_summary = data['currently']['summary']
        self.weather_temperature = data['currently']['temperature']
        return True
    def update_weather(self):
        full_url = "{0}{1}/{2},{3}".format(DARKSKYURL, DSKEY, self.lat, self.long)
        PARAMS = {'exclude': 'minutely,hourly,daily,alerts,flags'}
        r = requests.get(url = full_url, params = PARAMS)
        data = r.json()
        self.weather_summary = data['currently']['summary']
        self.weather_temperature = data['currently']['temperature']
        return True
