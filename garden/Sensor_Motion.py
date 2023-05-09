import RPi.GPIO as GPIO
import time
import subprocess
from datetime import datetime
import os 
from sensor_bme680 import call_bme680


# Set the GPIO mode to BCM numbering
GPIO.setmode(GPIO.BCM)

# Define the input pin for the sensor and output pin for the camera trigger
pir_sensor = 23
camera_trigger = 24

# Set up the input pin as a pull-down input and the output pin as a GPIO output
GPIO.setup(pir_sensor, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(camera_trigger, GPIO.OUT)

# Define a callback function to be called when motion is detected
def motion_detected(channel):
    print("Motion detected! Taking a picture...")
    
    # Trigger the camera module
    GPIO.output(camera_trigger, GPIO.HIGH)
    time.sleep(0.5)
    GPIO.output(camera_trigger, GPIO.LOW)
    
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    
    directory = os.path.join(os.path.expanduser("~"), "busted_pictures")
    if not os.path.exists(directory):
        os.makedirs(directory)
        
    # Take a picture and save it to a file
    filename = os.path.join(directory, "motion_picture_{}.jpg".format(timestamp))

    subprocess.call(["raspistill", "-o", filename])
    print("Picture taken and saved as", filename)

# Add the callback function to the sensor input
GPIO.add_event_detect(pir_sensor, GPIO.RISING, callback=motion_detected)

# Main loop
try:
    while True:
        time.sleep(1)

except KeyboardInterrupt:
    print("Program stopped by user")
    
finally:
    GPIO.cleanup()