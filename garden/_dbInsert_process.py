from garden import models
from datetime import datetime

from views import call_sensors 


def insert_sensor_value():
    
    try:
        results = call_sensors()
        air_temp = results['air_temp']['value'] if 'air_temp' in results else None
        pressure = results['pressure']['value'] if 'pressure' in results else None
        air_hum = results['air_hum']['value'] if 'air_hum' in results else None
        soil_hum = results['soil_hum']['value'] if 'soil_hum' in results else None
        soil_temp = results['soil_temp']['value'] if 'soil_temp' in results else None
        light = results['light']['value'] if 'light' in results else None

        # handle the case where a sensor value is missing
        if None in (air_temp, pressure, air_hum, soil_hum, soil_temp, light):
            return ({"code": 400, "message": "missing sensor value"})


        # handle the case where results is not a dictionary
        sensor_value = []
        sensor_value = models.SensorValue.objects.create(
            air_temp=air_temp,
            pressure=pressure,
            air_hum=air_hum,
            soil_hum=soil_hum,
            soil_temp=soil_temp,
            light=light,
            timestamp=datetime.now(),
        )
    except:
        # handle all other exceptions
        return ({"code": 400, "message": "An error occurred while reading and preparing data"})
    else:
        # execute if no exception was raised in the try block
        # return a response indicating that the record was inserted
        return ({"code": 200, "message": "successfully added", "data": results})
