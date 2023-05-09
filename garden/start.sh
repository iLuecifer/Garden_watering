#!/bin/bash
source /home/it/garden_watering/venv/bin/activate

export PYTHONPATH=/home/it/garden_watering:$PYTHONPATH

# Start the Django server
python manage.py runserver 8999 &
django_pid=$!

# Start the _motion_process
python /home/it/garden_watering/garden/_motion_process.py &
motion_pid=$!

# Start the _dbInsert_process
python /home/it/garden_watering/garden/_dbInsert.py &
dbinsert_pid=$!

cd frontend
# Start the npm server
npm start &
server_pid=$!

cd ..
# Save the process IDs to a file for later use
echo $motion_pid $dbinsert_pid $django_pid $server_pid > /home/it/garden_watering/garden/pids.txt

# Define a function to stop the processes gracefully
function stop_processes {
    kill $(cat /home/it/garden_watering/garden/pids.txt)
    rm /home/it/garden_watering/garden/pids.txt
}

# Register the function to be called on SIGTERM and SIGINT signals
trap stop_processes SIGTERM SIGINT

# Wait for the processes to terminate
wait

cd frontend
npm stop
