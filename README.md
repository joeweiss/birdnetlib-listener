# birdnetlib-listener

## Running in Docker

### Raspberry Pi 4 - 64bit

Bring it up and run:
`docker compose -f docker-compose.rpi4.yml up -d --build`

To run the watcher/analyzer:
`docker compose -f docker-compose.rpi4.yml exec web python manage.py runscript analyze`

To run the Django test cases:
`docker compose -f docker-compose.rpi4.yml exec web python manage.py test`

To take it down:
`docker compose -f docker-compose.rpi4.yml down`

To run bash within the docker instance:
`docker compose -f docker-compose.rpi4.yml exec web bash`

To rebuild the image for a reason (e.g. after pip change)
`docker compose -f docker-compose.rpi4.yml down; docker compose -f docker-compose.rpi4.yml build --no-cache`

### MacOS M1

Bring it up and run:
`docker compose -f docker-compose.macm1.yml up -d --build`

To run the watcher/analyzer:
`docker compose -f docker-compose.macm1.yml exec web python manage.py runscript analyze`

To run the Django test cases:
`docker compose -f docker-compose.macm1.yml exec web python manage.py test`

To take it down:
`docker compose -f docker-compose.macm1.yml down`

To run bash within the docker instance:
`docker compose -f docker-compose.macm1.yml exec web bash`

To rebuild the image for a reason (e.g. after pip change)
`docker compose -f docker-compose.macm1.yml down; docker compose -f docker-compose.macm1.yml build --no-cache`

## Recording audio

The docker container itself does not record audio to the `audio_inbox` directory. See below for basic examples for recording 30-second properly-dated WAV files to audio_inbox.

### Raspberry Pi 4

Prerequisites: arecord

To record an audio stream to "audio_inbox", run the following.
`python script_examples/audio_recording_rpi.py`

### MacOS M1

Prerequisites: sox, pysox

To record an audio stream to "audio_inbox", run the following.
`python script_examples/audio_recording_macos.py`

## Putting it all together

In order to create a self-running, restart-tolerant installation, you'll need to setup a few extra things. For example, the setup for a Raspberry Pi 4 is provided below. Other systems will require other methods of starting and restarting the processes.

Prerequisites: Raspberry Pi 4 with clean 64-bit system, `docker`, `docker-compose` and `arecord`.

### Confirm that the system works

In one terminal, run:

```
mkdir audio_inbox
mkdir audio_post_analyze
docker compose -f docker-compose.rpi4.yml up -d --build
docker compose -f docker-compose.rpi4.yml exec web python manage.py runscript analyze
```

In another terminal, start the recording:

```
python script_examples/audio_recording_macos.py
```

### Setup systemd to auto-start the analyze and recording processes on boot

<snip> More to come ...
