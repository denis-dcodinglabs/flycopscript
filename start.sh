#!/bin/sh
# start.sh
# Run the Python scripts in the background
python3 prishtinaticket.py &
python3 rfly.py &
python3 kosfly.py &
python3 flyska.py &
python3 ark.py &
python3 airpristina.py &
# Start the gunicorn servers on different ports
gunicorn -b :8080 filterApi:app