import os
import time
import logging

stop_signal_file = '/tmp/stop_signal.txt'
logging.info('Motion detection daemon started')
while True:
    if os.path.exists(stop_signal_file):
        # stop signal file exists, exit loop
        logging.info('Stop signal file detected, exiting...')
        break
    logging.info('file not found proceeding  ...')
    # main daemon process logic here
    # separate_process.py in the separate process
    import daemon
    import signal

    def run():
        import requests
        import RPi.GPIO as GPIO
        import os
        import subprocess
        import time
        from datetime import datetime

        # Set up the GPIO pins
        GPIO.setmode(GPIO.BCM)
        pir_sensor = 12
        camera_trigger = 24
        GPIO.setup(pir_sensor, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(camera_trigger, GPIO.OUT)

        # Define a function to take a picture when motion is detected
        def detect_motion(channel):
            # Trigger the camera module
            GPIO.output(camera_trigger, GPIO.HIGH)
            time.sleep(0.5)
            GPIO.output(camera_trigger, GPIO.LOW)

            # Save the picture to a file
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            directory = os.path.join(os.path.expanduser("~"), "busted_pictures")
            if not os.path.exists(directory):
                os.makedirs(directory)
            filename = os.path.join(directory, "motion_picture_{}.jpg".format(timestamp))
            subprocess.call(["raspistill", "-o", filename])
            print("Picture taken and saved as", filename)

        # Set up the PIR sensor to call the detect_motion function when motion is detected
        GPIO.add_event_detect(pir_sensor, GPIO.RISING, callback=detect_motion)

        # Listen for messages
        while True:
            # Check for messages in a message queue or a database
            # For simplicity, we'll just use a REST API call to a Django endpoint
            response = requests.get("http://172.0.0.1:8999/api/motion_detection/")
            if response.status_code == 200:
                message = response.json()
                if message["command"] == "start":
                    # Start monitoring the PIR sensor
                    try:
                        while True:
                            time.sleep(1)
                    except KeyboardInterrupt:
                        GPIO.cleanup()
                        print("Motion detection stopped")
                elif message["command"] == "stop":
                    logging.info('stopping bcz of command stop')
                    # Stop monitoring the PIR sensor
                    GPIO.cleanup()
                else:
                    print("Invalid command")
            else:
                print("Failed to retrieve command")


    def stop(signum, frame):
        # This function will be called when the daemon is stopped
        raise SystemExit

    if __name__ == '__main__':
        # Register the stop function to be called when the daemon is stopped
        signal.signal(signal.SIGTERM, stop)

        # Start the daemon
        with daemon.DaemonContext():
            run()
    
    time.sleep(1)

# cleanup and exit
os.remove(stop_signal_file)
logging.info('File removed')