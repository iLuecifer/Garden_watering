import os
import time
import logging
import signal
import requests
import RPi.GPIO as GPIO
import subprocess
from datetime import datetime
from daemon import DaemonContext

class MotionDetectionDaemon:
    def __init__(self):
        self.stop_signal_file = 'garden/stop_signal/stop_signal.txt'
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
    
        handler = logging.FileHandler('garden/log/motion_detection_daemon.log')
        handler.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.debug("Handler added to logger")
        self.pir_sensor = 12
        self.camera_trigger = 24

    def run(self):
        
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pir_sensor, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.camera_trigger, GPIO.OUT)

        def detect_motion(channel):
            GPIO.output(self.camera_trigger, GPIO.HIGH)
            time.sleep(0.5)
            GPIO.output(self.camera_trigger, GPIO.LOW)

            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            directory = os.path.join(os.path.expanduser("~"), "busted_pictures")
            if not os.path.exists(directory):
                os.makedirs(directory)
            filename = os.path.join(directory, "motion_picture_{}.jpg".format(timestamp))
            subprocess.call(["raspistill", "-o", filename])
            self.logger.debug("Picture taken and saved as %s", filename)

        GPIO.add_event_detect(self.pir_sensor, GPIO.RISING, callback=detect_motion)

        while True:
            if os.path.exists(self.stop_signal_file):
                self.logger.debug('Stop signal file detected, exiting...')
                break

            response = requests.get("http://172.0.0.1:8999/api/motion_detection/")
            if response.status_code == 200:
                message = response.json()
                if message["command"] == "start":
                    try:
                        while True:
                            time.sleep(1)
                    except KeyboardInterrupt:
                        GPIO.cleanup()
                        self.logger.debug("Motion detection stopped")
                elif message["command"] == "stop":
                    self.logger.debug('Stopping motion detection...')
                    GPIO.cleanup()
                else:
                    self.logger.debug("Invalid command")
            else:
                self.logger.error("Failed to retrieve command")

    def stop(self):
        self.logger.debug('Received stop signal, exiting...')
        os.remove(self.stop_signal_file)
        raise SystemExit

if __name__ == '__main__':
    daemon = MotionDetectionDaemon()

    with DaemonContext():
        signal.signal(signal.SIGTERM, daemon.stop)
        while True:
            daemon.run()
            time.sleep(1)
