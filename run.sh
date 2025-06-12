#!/bin/bash

# Start baresip_monitor using module syntax
echo "Starting baresip_monitor..."
python3 -m app.main &

# Start the web_gui using Gunicorn
echo "Starting web_gui with Gunicorn..."
gunicorn app.web_gui:app --bind 0.0.0.0:8000 &

echo "Both services have been started."

wait -n
