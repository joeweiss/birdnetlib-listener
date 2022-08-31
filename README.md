# birdnetlib-listener

## Running in Docker

Bring it up and run:
docker compose up -d --build

To run the watcher/analyzer:
docker compose exec web python manage.py runscript analyze

To run the Django test cases:
docker compose exec web python manage.py test

To take it down:
docker compose down

To run bash within the docker instance:
docker compose exec web bash

To rebuild the image for a reason (e.g. after pip change)
docker compose down; docker compose build --no-cache
