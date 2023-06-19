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



## Raspberry Pi 4 (2021 era board, 2023 Raspbian)

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

```

Install pip3
`sudo apt-get install python3-pip`

Install docker-compose
`sudo pip3 install docker-compose`

Confirm docker works:
`docker run hello-world`

If you get a permission error, try this:
`sudo chmod 666 /var/run/docker.sock`

Build the initial image

This may take 10-12 minutes.

`docker compose -f docker-compose.rpi.yml up -d --build`


Start the recorder
`python script_examples/audio_recording_rpi.py`

In another terminal, start the analyzers.

`docker compose -f docker-compose.rpi.yml exec web python manage.py runscript analyze`

Set docker to start on boot.
`sudo systemctl enable docker`

Copy recording service

`sudo cp recording.service /etc/systemd/system/recording.service; sudo systemctl daemon-reload; sudo systemctl start recording; systemctl status recording.service`

Allow login to linger for the user (for pulseaudio to prevent /run/user/1000/pulse error)

`sudo loginctl enable-linger $USER`
