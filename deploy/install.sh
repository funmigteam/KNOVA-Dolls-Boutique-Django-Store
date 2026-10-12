#!/bin/bash
set -euo pipefail
if [ "$(id -u)" -ne 0 ]; then
    echo 'Run this script with sudo.' >&2
    exit 1
fi
APP='/srv/knova'
DEPLOY="$APP/deploy"
test -x /srv/knova/.venv/bin/python
test -s /srv/knova/production.env
install -d -m 0750 /etc/knova
if [ ! -f /etc/knova/production.env ]; then
    install -m 0600 /srv/knova/production.env /etc/knova/production.env
fi
install -d -m 0700 /etc/nginx/knova-tls
if [ ! -s /etc/nginx/knova-tls/origin.crt ]; then
    openssl req -x509 -newkey rsa:2048 -nodes -days 365 \
        -keyout /etc/nginx/knova-tls/origin.key \
        -out /etc/nginx/knova-tls/origin.crt \
        -subj '/CN=knova.ir' \
        -addext 'subjectAltName=DNS:knova.ir,DNS:www.knova.ir'
    chmod 0600 /etc/nginx/knova-tls/origin.key
fi
install -m 0644 "$DEPLOY/knova.service" /etc/systemd/system/knova.service
install -m 0644 "$DEPLOY/knova.conf" /etc/nginx/sites-available/knova.conf
ln -sfn /etc/nginx/sites-available/knova.conf /etc/nginx/sites-enabled/knova.conf
if ! /usr/sbin/nginx -t; then
    rm /etc/nginx/sites-enabled/knova.conf
    exit 1
fi
runuser -u www-data -- test -r "$APP/staticfiles/css/style.css"
systemctl daemon-reload
systemctl enable knova.service
systemctl restart knova.service
for attempt in {1..15}; do
    if curl --fail --silent -H 'Host: knova.ir' -H 'X-Forwarded-Proto: https' http://127.0.0.1:8014/ -o /dev/null; then
        systemctl reload nginx
        curl --fail --silent -H 'Host: knova.ir' -H 'X-Forwarded-Proto: https' http://127.0.0.1/ -o /dev/null
        curl --fail --silent -H 'Host: knova.ir' http://127.0.0.1/static/css/style.css -o /dev/null
        systemctl --no-pager status knova.service
        exit 0
    fi
    sleep 1
done
journalctl -u knova.service -n 30 --no-pager
exit 1
