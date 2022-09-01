# birdnetlib-listener

## Running in Docker

### Raspberry Pi 4 - 64bit

Bring it up and run:
docker compose -f docker-compose.rpi4.yml up -d --build

To run the watcher/analyzer:
docker compose -f docker-compose.rpi4.yml exec web python manage.py runscript analyze

To run the Django test cases:
docker compose -f docker-compose.rpi4.yml exec web python manage.py test

To take it down:
docker compose -f docker-compose.rpi4.yml down

To run bash within the docker instance:
docker compose -f docker-compose.rpi4.yml exec web bash

To rebuild the image for a reason (e.g. after pip change)
docker compose -f docker-compose.rpi4.yml down; docker compose build --no-cache

### MacOS M1

Bring it up and run:
docker compose -f docker-compose.macm1.yml up -d --build

To run the watcher/analyzer:
docker compose -f docker-compose.macm1.yml exec web python manage.py runscript analyze

To run the Django test cases:
docker compose -f docker-compose.macm1.yml exec web python manage.py test

To take it down:
docker compose -f docker-compose.macm1.yml down

To run bash within the docker instance:
docker compose -f docker-compose.macm1.yml exec web bash

To rebuild the image for a reason (e.g. after pip change)
docker compose -f docker-compose.macm1.yml down; docker compose build --no-cache

## Recording audio

The docker container itself does not record audio to audio_inbox directory. See below for basic examples for recording 30-second long WAV files to audio_inbox.

### Raspberry Pi 4

To record an audio stream to "audio_inbox", run the following.
`python script_examples/audio_recording_rpi.py`

### MacOS M1

Prerequisites: sox

To record an audio stream to "audio_inbox", run the following.
`python script_examples/audio_recording_macosm1.py`
