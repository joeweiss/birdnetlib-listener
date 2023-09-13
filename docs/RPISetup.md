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
