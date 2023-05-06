#!/bin/bash

# Start the Django server
python manage.py runserver 8999 &
django_pid=$!

# Start the _motion_process
python /home/it/garden_watering/garden/_motion_process.py &
motion_pid=$!

# Start the _dbInsert_process
python /home/it/garden_watering/garden/_dbInsert_process.py &
dbinsert_pid=$!


# Save the process IDs to a file for later use
echo $motion_pid $dbinsert_pid $django_pid > /home/it/garden_watering/garden/pids.txt

# Wait for a signal to stop the processes
trap "kill $(cat /home/it/garden_watering/garden/pids.txt)" SIGTERM SIGINT

# Wait for the processes to terminate
wait
