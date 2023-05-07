from time import sleep
import os
import django 
#import sys
# Add the path to the "garden" package to the PYTHONPATH
#sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'garden')))

# Set the environment variable for Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "garden_watering.settings")
django.setup()
from garden.views import insert_sensor_value

while True:
    print("starting")
    response = insert_sensor_value()
    print(response)
    sleep(300)
