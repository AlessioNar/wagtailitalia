#!/bin/bash

NAME=$1
DOMAIN=$2
USER=$3

## Supervisor configuration
cp ./config/"${NAME}".conf /etc/supervisor/conf.d/"${NAME}".conf

## Gunicorn configuration
cp ./config/gunicorn_start /home/"${USER}"/"${DOMAIN}"/"${NAME}"-env/bin/gunicorn_start

## Copy Nginx configuration
cp ./config/nginx_nocert/"${DOMAIN}" /etc/nginx/sites-available/"${DOMAIN}"

# Set up manage.py to use production settings
cp ./config/manage.py ./manage.py

# Create symbolic link for domain
ln -s /etc/nginx/sites-available/"${DOMAIN}" /etc/nginx/sites-enabled/

# Set up postgresql database

## Set up environmental variables for production environment
#scp -r  "${SOURCE_DIR}"/"${NAME}"/".env" "${USER}"@"${IP_ADDRESS}":/home/"${USER}"/"${DOMAIN}"/.env

# Create a random SECRET_KEY and append it as an environmental variable
#openssl rand >> .env

# Activate virtual environment
source ./"${NAME}"-env/bin/activate && \
# Update pip and migrate database
pip install -r ./requirements.txt && \
python ./manage.py collectstatic --noinput && \
python ./manage.py makemigrations && \
python ./manage.py migrate && \
python ./manage.py load

# Prompt the user to create at least a super user 

# Restart Supervisor
supervisorctl restart $NAME
systemctl restart nginx

exit 0

# Copy media folder
#scp -r  "${SOURCE_DIR}"/"${NAME}"/"media" "${USER}"@"${IP_ADDRESS}":/home/"${USER}"/"${DOMAIN}"/media

# Setting up SSL connection
if [ $4 == '--ssl']; then
    certbot certonly --agree-tos --email "${EMAIL}" -d "${DOMAIN}"
    cp ./config/nginx_cert/"${DOMAIN}" /etc/nginx/sites-available/"${DOMAIN}"
fi

exit 0
