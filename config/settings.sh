#!/bin/bash

NAME=$1
DOMAIN=$2
USER=$3

## Supervisor configuration
cp ./config/"${NAME}".conf /etc/supervisor/conf.d/"${NAME}".conf

## Gunicorn configuration
cp ./config/gunicorn_start /home/"${USER}"/"${DOMAIN}"/"${NAME}"-env/bin/gunicorn_start
sudo chmod g+wx /home/"${USER}"/"${DOMAIN}"/"${NAME}"-env/bin/gunicorn_start

## Copy Nginx configuration
cp ./config/nginx_nocert/"${DOMAIN}" /etc/nginx/sites-available/"${DOMAIN}"

# Set up manage.py to use production settings
cp ./config/manage.py ./manage.py

# Create symbolic link for domain, if it does not exist
ln -s /etc/nginx/sites-available/"${DOMAIN}" /etc/nginx/sites-enabled/


