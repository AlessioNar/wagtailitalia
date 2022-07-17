#!/bin/bash

NAME=$1
DOMAIN=$2

sudo supervisorctl stop $NAME
sudo supervisorctl remove $NAME
sudo rm /etc/supervisor/conf.d/${NAME}.conf
sudo rm -rf /home/admin/${DOMAIN}
sudo rm -rf /home/admin/logs/${NAME}

psql -c 'DROP DATABASE '$NAME';'
sudo rm /etc/nginx/sites-enabled/${DOMAIN}
sudo rm /etc/nginx/sites-available/${DOMAIN}

sudo systemctl restart nginx