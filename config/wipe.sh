#!/bin/bash

NAME=$1
DOMAIN=$2

sudo supervisorctl stop $NAME
sudo supervisorctl remove $NAME
sudo rm /etc/supervisor/conf.d/${NAME}.conf


if [ -z $DOMAIN ]; then
    echo "Domain not specified"
else
    rm -rf /home/admin/${DOMAIN}
    rm -rf /home/admin/logs/${NAME}
    sudo rm /etc/nginx/sites-enabled/${DOMAIN}
    sudo rm /etc/nginx/sites-available/${DOMAIN}
    
fi

sudo -u postgres psql -c 'DROP DATABASE '$NAME';'

sudo systemctl restart nginx