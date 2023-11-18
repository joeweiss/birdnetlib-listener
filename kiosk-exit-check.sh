#!/bin/bash

# Define the path to the file you want to check for
file_to_check="/home/mccaskey/Code/birdnetlib-listener-device/audio/kill-kiosk.txt"

while true; do
    # Check if the file exists
    if [ -e "$file_to_check" ]; then
        # If the file exists, stop Chrome using pkill
        pkill chrome
        echo "Chrome has been stopped."

        # Remove the file
        rm "$file_to_check"
        echo "File has been deleted."
    else
        echo "File does not exist. Chrome is not stopped."
    fi
    
    # Sleep for 10 seconds before checking again
    sleep 10
done
