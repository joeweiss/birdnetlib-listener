#!/bin/bash

# Delay so the docker container has time to start.
sleep 20

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
