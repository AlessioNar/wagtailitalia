#!/bin/bash

NAME=$1
DOMAIN=$2
USER=$3

## Gunicorn configuration
#cp ./config/gunicorn/gunicorn_start /home/"${USER}"/"${DOMAIN}"/"${NAME}"-env/bin/gunicorn_start
#sudo chmod g+wx /home/"${USER}"/"${DOMAIN}"/"${NAME}"-env/bin/gunicorn_start

# Setting up Systemd configuration 
#sudo cp ./config/systemd/gunicorn.service /etc/systemd/system/gunicorn.service
#sudo cp ./config/systemd/gunicorn.socket /etc/systemd/system/gunicorn.socket

# Supervisor configuration
sudo cp ./config/supervisor/wagtailitalia.conf /etc/supervisor/conf.d/"${NAME}".conf

## Copy Nginx configuration
cp ./config/nginx/nginx_nocert/wagtail-italia.it /etc/nginx/sites-available/"${DOMAIN}"

# Set up manage.py to use production settings
cp ./config/manage.py ./manage.py

# Create symbolic link for domain, if it does not exist
ln -s /etc/nginx/sites-available/"${DOMAIN}" /etc/nginx/sites-enabled/

exit
