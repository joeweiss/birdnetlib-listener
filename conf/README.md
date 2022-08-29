Change nginx config

```
sudo cp listener.conf /etc/nginx/sites-available/
sudo systemctl reload nginx
```

Change uwsgi config

```

sudo systemctl stop uwsgi
sudo cp uwsgi.service /etc/systemd/system/uwsgi.service
sudo systemctl daemon-reload
sudo systemctl start uwsgi

```
