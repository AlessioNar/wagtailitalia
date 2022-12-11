#!/bin/bash

# This script is executed after a site is created
# It copies the nginx configuration file and creates a symbolic link

SITE_NAME=$1
DOMAIN=$2
USERNAME=$3

## Copy Nginx configuration
cp ./config/nginx/nginx_nocert/wagtail-italia.it /etc/nginx/sites-available/"${DOMAIN}"
echo "Copied Nginx configuration"

# Set up manage.py to use production settings
cp ./config/manage.py ./manage.py

# Create symbolic link for domain, if it does not exist
ln -s /etc/nginx/sites-available/"${DOMAIN}" /etc/nginx/sites-enabled/
echo "Created symbolic link for domain"

exit 0
