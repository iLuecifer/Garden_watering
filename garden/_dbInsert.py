from time import sleep
import os
import django
import json 
#import sys
# Add the path to the "garden" package to the PYTHONPATH
#sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'garden')))

# Set the environment variable for Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "garden_watering.settings")
django.setup()
from garden.utils import insert_sensor_value, enable_relais, disable_relais


while True:
    print("starting")
    response = insert_sensor_value()
    # Open the JSON file
    with open('/home/it/garden_watering/garden/critical_values.json', 'r') as file:
        # Load the JSON data as a Python object
        criticalValues = json.load(file)

    if response["code"] == 200:  # Check if the response code is 200 (success)
        if response["data"]["soil_hum"]["value"] < criticalValues["soil_hum_critical_min"]:
            enable_relais()
        elif response["data"]["soil_hum"]["value"] > criticalValues["soil_hum_critical_max"]:
            disable_relais()
        print(response)
    else:
        print("Error in response:", response["message"])

    sleep(300)

