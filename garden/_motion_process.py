import os
import time
import logging
import RPi.GPIO as GPIO
import subprocess
from datetime import datetime


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
    GPIO.output(camera_trigger, GPIO.HIGH)
    time.sleep(0.5)
    GPIO.output(camera_trigger, GPIO.LOW)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    directory = os.path.join(os.path.expanduser("~"), "busted_pictures")
    if not os.path.exists(directory):
        os.makedirs(directory)
    filename = os.path.join(directory, "motion_picture_{}.jpg".format(timestamp))
    subprocess.call(["raspistill", "-o", filename])
    logger.debug("Picture taken and saved as %s", filename)

GPIO.add_event_detect(pir_sensor, GPIO.RISING, callback=detect_motion)

while True:
    logger.info(stop_signal_file)
    if os.path.exists(stop_signal_file):
        logger.info("Stop signal file detected, exiting")
        logger.debug('Stop signal file detected, exiting...')
        break

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        GPIO.cleanup()
        logger.debug("Motion detection stopped")
        logger.info("Motion detection stopped")
