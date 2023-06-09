
from django.conf import settings
from django.db import models
from django.contrib.auth.models import User

class SensorValue(models.Model):
    id = models.AutoField(primary_key=True)
    air_temp = models.FloatField()
    pressure = models.FloatField()
    air_hum = models.FloatField()
    soil_hum = models.FloatField()
    soil_temp = models.FloatField()
    light = models.FloatField()
    timestamp = models.DateTimeField()
    status = models.BooleanField(default=False)
    class Meta:
        app_label = 'garden'

class BustedPictures(models.Model):
    id = models.AutoField(primary_key = True)
    picture = models.ImageField(upload_to='busted_pictures/')
    timestamp = models.DateTimeField(auto_now=True)
    class Meta:
        app_label = 'garden'

class WaterPumpeLogs(models.Model):
    id = models.AutoField(primary_key = True)
    start = models.DateTimeField(auto_now=True)
    end = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    class Meta:
        app_label = 'garden'


