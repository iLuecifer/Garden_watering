from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import bme680#bme680
from adafruit_seesaw.seesaw import Seesaw
import board
import smbus#BH1750
import json 
from django.views.decorators.csrf import csrf_exempt
from .models import SensorValue
from datetime import datetime
from django.core import serializers

def my_view(request):

    results = call_sensors()                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  
    if not len(results) == 0:
        return JsonResponse({"results": results})
    else:
        return JsonResponse({"text": "kein Daten"})

def call_sensors():

    results = dict(s_bme680())
    seesaw_results = dict(s_seesaw())
    results.update(seesaw_results)

    bh_results = dict(call_bh1750())
    results.update(bh_results)

    return results

def s_seesaw():
    #seesaw
    i2c_bus = board.I2C()
    ss = Seesaw(i2c_bus, addr=0x36)
    # read moisture level through capacitive touch pad
    touch = ss.moisture_read()
    # read temperature from the temperature sensor
    temp = ss.get_temp()

    results = {}
    results['soil_hum'] = {'value': touch, 'unit': 'x'}
    results['soil_temp'] = {'value': temp, 'unit': 'C'}
    return results


def s_bme680(): 
    sensor = bme680.BME680(i2c_addr=bme680.I2C_ADDR_SECONDARY)
    sensor.set_humidity_oversample(bme680.OS_2X)
    sensor.set_pressure_oversample(bme680.OS_4X)
    sensor.set_temperature_oversample(bme680.OS_8X)
    sensor.set_filter(bme680.FILTER_SIZE_3)

    sensor.set_gas_status(bme680.ENABLE_GAS_MEAS)
    sensor.set_gas_heater_temperature(320)
    sensor.set_gas_heater_duration(150)
    sensor.select_gas_heater_profile(0)

    results = {}
    results['air_temp'] = {'value': sensor.data.temperature, 'unit': 'C'}
    results['pressure'] = {'value': sensor.data.pressure, 'unit': 'hPa'}
    results['air_hum'] = {'value': sensor.data.humidity, 'unit': '%'}
    if sensor.data.heat_stable:
        results['gas_resist'] = {'value': sensor.data.gas_resistance, 'unit': 'Ohm'}
    
    return results

#for bh1750
def convertToNumber(data):
    result=(data[1] + (256 * data[0])) / 1.2
    return (result)

def call_bh1750():
    DEVICE     = 0x23 #for BH1750
    POWER_DOWN = 0x00
    POWER_ON   = 0x01
    RESET      = 0x07
    bus = smbus.SMBus(1)

    data = bus.read_i2c_block_data(DEVICE,0x20)
    lightLevel = convertToNumber(data)
    return {'light':{'value': format(lightLevel,'.2f'), 'unit': 'lux'}}
#def messwerte_lesen(request):
 #   return HttpResponse(call_bme680())

def insert_sensor_value(request):
    
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
            return JsonResponse({"code": 400, "message": "missing sensor value"})


        # handle the case where results is not a dictionary
        sensor_value = []
        sensor_value = SensorValue.objects.create(
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
        return JsonResponse({"code": 400, "message": "An error occured while reading and preparing data"})
    else:
        # execute if no exception was raised in the try block
        # return a response indicating that the record was inserted
        return JsonResponse({"code": 200, "message": "successfully added", "data": results})

def getAllSensorData(request):
    all_sensor_values = SensorValue.objects.all()
    data = serializers.serialize('json', all_sensor_values)
    return JsonResponse(data, safe=False)


