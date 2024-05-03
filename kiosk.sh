#!/bin/bash

# Delay so the docker container has time to start.
url="http://127.0.0.1:8000"  # Replace with the URL you want to check
status_code=0

# Loop until a 200 OK response is received
until [ "$status_code" -eq 200 ]; do
    echo "Checking URL..."
    # Use curl to get the HTTP status code
    status_code=$(curl -o /dev/null -s -w "%{http_code}\n" "$url")

    if [ "$status_code" -eq 200 ]; then
        echo "Received 200 OK, continuing..."
    else
        echo "Service unavailable, retrying..."
        sleep 2  # Wait for 10 seconds before retrying
    fi
done


# Update from github
cd /home/pi/Code/birdnetlib-listener-device; git pull
cd /home/pi/Code/birdnetlib-listener-device; docker compose -f docker-compose.rpi.yml exec web python manage.py migrate

xset s noblank
xset s off
xset -dpms

unclutter -idle 0.5 -root &

sed -i 's/"exited_cleanly":false/"exited_cleanly":true/' /home/pi/.config/chromium/Default/Preferences
sed -i 's/"exit_type":"Crashed"/"exit_type":"Normal"/' /home/pi/.config/chromium/Default/Preferences

/usr/bin/chromium-browser --noerrdialogs --disable-infobars --kiosk "http://localhost:8000/static/dist/index.html" --disk-cache-dir=/dev/null --disk-cache-size=1 &

while true; do
   # xdotool keydown ctrl+Tab; xdotool keyup crtl+Tab;
   sleep 5
done
