#!/bin/bash

# Start the daemon process
python /home/it/garden_watering/garden/_motion_process.py &

# Start the Django server
python manage.py runserver 8999
