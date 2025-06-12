#!/bin/bash

# Start the baresip_monitor (make sure main.py only starts baresip_monitor)
echo "Starting baresip_monitor..."
python3 app/main.py &

# Start the web_gui using Gunicorn (adjust module path if necessary)
echo "Starting web_gui with Gunicorn..."
gunicorn app.web_gui:app --bind 0.0.0.0:8000 &

echo "Both services have been started."

wait -n
