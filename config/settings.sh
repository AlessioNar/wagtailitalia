#!/bin/bash

NAME=$1
DOMAIN=$2
USER=$3
DB_PASSWORD=$4

## Supervisor configuration
cp ./config/"${NAME}".conf /etc/supervisor/conf.d/"${NAME}".conf

## Gunicorn configuration
cp ./config/gunicorn_start /home/"${USER}"/"${DOMAIN}"/"${NAME}"-env/bin/gunicorn_start

## Copy Nginx configuration
cp ./config/nginx_nocert/"${DOMAIN}" /etc/nginx/sites-available/"${DOMAIN}"

# Set up manage.py to use production settings
cp ./config/manage.py ./manage.py

# Create symbolic link for domain, if it does not exist
ln -s /etc/nginx/sites-available/"${DOMAIN}" /etc/nginx/sites-enabled/

# Set up postgresql database
createdb --owner $USER $NAME

echo DB_NAME=$NAME >> .env
echo DB_USER=$USER >> .env
echo DB_PASSWORD=$DB_PASSWORD >> .env

# Generate a random SECRET_KEY and append it as an environmental variable
secret_key=$(openssl rand -base64 100 | tr -d '\n')
echo SECRET_KEY=$secret_key >> .env

# Launch application initialization process
source ./"${NAME}"-env/bin/activate && \
pip install -r ./requirements.txt && \
python ./manage.py collectstatic --noinput && \
python ./manage.py makemigrations && \
python ./manage.py migrate && \
python ./manage.py load

# Prompt the user to create at least a super user 

# Making supervisor aware of the new application

# Starting the application with supervisor
supervisorctl restart $NAME

# Restart Supervisor

systemctl restart nginx

# Copy media folder
#scp -r  "${SOURCE_DIR}"/"${NAME}"/"media" "${USER}"@"${IP_ADDRESS}":/home/"${USER}"/"${DOMAIN}"/media

# Setting up SSL connection
if [ $4 == '--ssl']; then
    certbot certonly --agree-tos --email "${EMAIL}" -d "${DOMAIN}"
    cp ./config/nginx_cert/"${DOMAIN}" /etc/nginx/sites-available/"${DOMAIN}"
fi

exit 0
