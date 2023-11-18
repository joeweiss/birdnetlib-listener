# Recent Raspberry Pi setup docs


## Raspberry Pi 3b+ (2017 era)

Fresh install with Raspberry Pi OS 64bit

Install pulseaudio (only needed if you're using Raspberry Pi OS Lite)
`sudo apt install pulseaudio`

Install docker
```
sudo apt update && sudo apt upgrade -VV

# Reboot after update/upgrade.
sudo reboot

curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

sudo usermod -aG docker ${USER}
# Log out and log back in

# Test docker.
docker run hello-world


```

Install pip3
`sudo apt-get install python3-pip`

Install docker-compose
`sudo pip3 install docker-compose`


Build the initial image

This may take 10-12 minutes.

`docker compose -f docker-compose.rpi.yml up -d --build`


Start the recorder
`python script_examples/audio_recording_rpi.py`

In another terminal, start the analyzers.

`docker compose -f docker-compose.rpi.yml exec web python manage.py runscript analyze`


## Setup services

```
# Setup docker to start on boot
sudo systemctl enable docker

```

```
# Edit to change paths to your own home directory
pico server/recording.service
pico server/analysis.service
pico server/browser-check.service


# Copy to service directory
sudo cp server/recording.service /etc/systemd/system/
sudo cp server/analysis.service /etc/systemd/system/
sudo cp server/browser-check.service /etc/systemd/system/


# Start the service
sudo systemctl start recording.service
sudo systemctl start analysis.service
sudo systemctl start browser-check.service


# Check to see that it is running
sudo systemctl status recording.service
sudo systemctl status analysis.service
sudo systemctl status browser-check.service


# If all goes well, enable them both.
sudo systemctl enable recording.service
sudo systemctl enable analysis.service
sudo systemctl enable browser-check.service


# Reboot and confirm the services are running.
sudo reboot



```


## Setup kiosk mode

Mostly adapted from here:
https://www.raspberrypi.com/tutorials/how-to-use-a-raspberry-pi-in-kiosk-mode/

