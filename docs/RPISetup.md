# Recent Raspberry Pi setup docs


## Raspberry Pi 3b+ (2017 era)

Fresh install with Raspian 64bit

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

`docker compose -f docker-compose.rpi4.yml up -d --build`



