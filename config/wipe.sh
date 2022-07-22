#!/bin/bash

NAME=$1
DOMAIN=$2
sudo supervisorctl stop $NAME
sudo supervisorctl remove $NAME
sudo supervisorctl reread 

sudo rm /etc/supervisor/conf.d/${NAME}.conf
echo "Removed supervisor configuration"


if [ -z $DOMAIN ]; then
    echo "Domain not specified"
else
    sudo -u postgres psql -c 'DROP DATABASE '$NAME';'
    echo "Database removed"
    rm -rf /home/admin/${DOMAIN}
    echo "Removed ${DOMAIN} folder"
    rm -rf /home/admin/logs/${NAME}
    echo "Removed ${NAME} logs folder"
    sudo rm /etc/nginx/sites-enabled/${DOMAIN}
    echo "Removed ${DOMAIN} from nginx sites enabled"
    sudo rm /etc/nginx/sites-available/${DOMAIN}
    echo "Removed ${DOMAIN} from nginx sites available"
    
fi


sudo systemctl restart nginx
echo "Nginx restarted"