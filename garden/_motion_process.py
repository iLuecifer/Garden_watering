import os
import time
import logging
import RPi.GPIO as GPIO
import subprocess
from datetime import datetime
import django
from pathlib import Path
from datetime import datetime
import subprocess


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "garden_watering.settings")
django.setup()
from garden.models import BustedPictures

stop_signal_file = 'garden/stop_signal/stop_signal.txt'
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

handler = logging.FileHandler('garden/log/motion_detection_daemon.log')
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.debug("Handler added to logger")
logger.info("Handler added to logger")

pir_sensor = 12
camera_trigger = 24

GPIO.setmode(GPIO.BCM)
GPIO.setup(pir_sensor, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(camera_trigger, GPIO.OUT)


def detect_motion(channel):
    if os.path.exists(stop_signal_file):
        logger.info("Stop signal file detected, motion detection stopped")
        GPIO.remove_event_detect(pir_sensor)
        return

   
    logger.info("motion detected !")
    GPIO.output(camera_trigger, GPIO.HIGH)
    time.sleep(0.5)
    GPIO.output(camera_trigger, GPIO.LOW)
    logger.info("preparing to take a picture")

    directory = Path.home() / "busted_pictures"
    directory.mkdir(parents=True, exist_ok=True)


    now = datetime.now()
    TIMESTAMP = now.strftime("%Y-%m-%d_%H-%M-%S")
    filename = directory / f"motion_picture_{TIMESTAMP}.jpg"
    #subprocess.call(["raspistill", "-o", str(filename)])

    try:
        subprocess.run(["raspistill", "-o", str(filename)], check=True)
    except subprocess.CalledProcessError as e:
        logger.error("Error taking picture: %s", e)
    else:
        logger.info("Picture taken and saved as %s", filename)


    logger.info("Picture taken and saved as %s", filename)

    #time.sleep(1)
 
    
    #NSTAMP = now - timedelta(seconds=2)
    #TIMESTAMP_STR = NSTAMP.strftime("%Y-%m-%d_%H-%M-%S")
    #picture = BustedPictures()
    #with open(filename, 'rb') as file:
    #    picture.picture.save(os.path.basename(filename), file)
    #picture.timestamp = datetime.strptime(TIMESTAMP_STR, "%Y-%m-%d_%H-%M-%S")
    #picture.save()



GPIO.add_event_detect(pir_sensor, GPIO.RISING, callback=detect_motion)

try:
    while True:
        logger.info("testing stop signal...")
        if os.path.exists(stop_signal_file):
            logger.info("Stop signal file detected, motion detection stopped")
            GPIO.remove_event_detect(pir_sensor)
            while os.path.exists(stop_signal_file):
                time.sleep(1)
            logger.info("Stop signal file deleted, resuming process")
            GPIO.add_event_detect(pir_sensor, GPIO.RISING, callback=detect_motion)
        else:
            logger.info("stop signal file not found, motion detection started")
            GPIO.remove_event_detect(pir_sensor)
            GPIO.add_event_detect(pir_sensor, GPIO.RISING, callback=detect_motion)
            while not os.path.exists(stop_signal_file):
                if GPIO.event_detected(pir_sensor):
                    detect_motion(pir_sensor)
                    time.sleep(1)  # Add a short delay to avoid multiple detections
                else:
                    time.sleep(1)
except KeyboardInterrupt:
    GPIO.cleanup()
    logger.info("Motion detection stopped")


