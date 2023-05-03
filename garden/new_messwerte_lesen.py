import time#seesaw
import board
import smbus#BH1750
import time
import bme680#bme680
from adafruit_seesaw.seesaw import Seesaw


DEVICE     = 0x23 #for BH1750
POWER_DOWN = 0x00
POWER_ON   = 0x01
RESET      = 0x07
bus = smbus.SMBus(1)

#seesaw
i2c_bus = board.I2C()
ss = Seesaw(i2c_bus, addr=0x36)

#bme680
sensor = bme680.BME680(i2c_addr=bme680.I2C_ADDR_SECONDARY)

def call_bme680():
    sensor.set_humidity_oversample(bme680.OS_2X)
    sensor.set_pressure_oversample(bme680.OS_4X)
    sensor.set_temperature_oversample(bme680.OS_8X)
    sensor.set_filter(bme680.FILTER_SIZE_3)

    sensor.set_gas_status(bme680.ENABLE_GAS_MEAS)
    sensor.set_gas_heater_temperature(320)
    sensor.set_gas_heater_duration(150)
    sensor.select_gas_heater_profile(0)
    
    while True:
        if sensor.get_sensor_data():
            results = [['air_temp',sensor.data.temperature], ['pressure', sensor.data.pressure], ['air_hum', sensor.data.humidity]]
            if sensor.data.heat_stable:
                gasresist = ['gas_resist', sensor.data.gas_resistance]
                results.append(gasresist)
            return results

                

def call_seesaw():
    # read moisture level through capacitive touch pad
    touch = ss.moisture_read()
    # read temperature from the temperature sensor
    temp = ss.get_temp()
    return [['soil_hum',touch],['soil_temp', temp]]


       
#for bh1750
def convertToNumber(data):
    result=(data[1] + (256 * data[0])) / 1.2
    return (result)

def readLight(addr=DEVICE):
    data = bus.read_i2c_block_data(addr,0x20)
    return convertToNumber(data)


def call_bh1750():
    lightLevel=readLight()
    seesaw = call_seesaw()
    bme680 = call_bme680()
    return format(lightLevel,'.2f')
  
def start_measures():
    airResults = call_bme680()
    soilResults = call_seesaw()
    lightResults = call_bh1750()
    return [['airResults',airResults],['soilResults', soilResults], ['lightResults', lightResults]]
    
#if __name__=="__main__":
#   main()
    
