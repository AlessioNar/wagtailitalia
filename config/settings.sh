#!/bin/bash

NAME=$1
DOMAIN=$2
USER=$3

## Supervisor configuration
#cp ./config/wagtailitalia.conf /etc/supervisor/conf.d/"${NAME}".conf

## Gunicorn configuration
cp ./config/gunicorn_start /home/"${USER}"/"${DOMAIN}"/"${NAME}"-env/bin/gunicorn_start
sudo chmod g+wx /home/"${USER}"/"${DOMAIN}"/"${NAME}"-env/bin/gunicorn_start

# Setting up Systemd configuration 
sudo cp ./config/gunicorn.service /etc/systemd/system/gunicorn.service
sudo cp ./config/gunicorn.socket /etc/systemd/system/gunicorn.socket

## Copy Nginx configuration
cp ./config/nginx_nocert/wagtail-italia.it /etc/nginx/sites-available/"${DOMAIN}"

# Set up manage.py to use production settings
cp ./config/manage.py ./manage.py

# Create symbolic link for domain, if it does not exist
ln -s /etc/nginx/sites-available/"${DOMAIN}" /etc/nginx/sites-enabled/

exit
