import os
import time
import logging
import RPi.GPIO as GPIO
import subprocess
from datetime import datetime
# Set the environment variable for Django
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
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    directory = os.path.join(os.path.expanduser("~"), "busted_pictures")
    if not os.path.exists(directory):
        os.makedirs(directory)
    filename = os.path.join(directory, "motion_picture_{}.jpg".format(timestamp))
    subprocess.call(["raspistill", "-o", filename])
    logger.info("Picture taken and saved as %s", filename)

    picture = BustedPictures()
    picture.picture.save(filename, open(filename, 'rb'))
    picture.timestamp.save(datetime.datetime.now())
    picture.save()
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
            if not GPIO.event_detected(pir_sensor):
                time.sleep(1)
            else:
                detect_motion(pir_sensor)
except KeyboardInterrupt:
    GPIO.cleanup()
    logger.info("Motion detection stopped")
