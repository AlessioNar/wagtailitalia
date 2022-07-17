#! /bin/bash

NAME=$1
USER=$2
DB_PASSWORD=$3

# Print access credentials to the environmental variable
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
python ./manage.py makemigrations blog flex home streams menus site_settings websites && \
python ./manage.py migrate && \
python ./manage.py load

# Create superuser

mkdir ../logs/${NAME}
touch ../logs/${NAME}/gunicorn_supervisor.log
echo "Created log files"

# Making supervisor aware of the new application
sudo supervisorctl reread 
sudo supervisorctl add "${NAME}"

# Starting the application with supervisor
sudo supervisorctl start "${NAME}"

# Restart Nginx server
sudo systemctl restart nginx

exit 0

# Copy media folder
#scp -r  "${SOURCE_DIR}"/"${NAME}"/"media" "${USER}"@"${IP_ADDRESS}":/home/"${USER}"/"${DOMAIN}"/media

# Setting up SSL connection
 if [ "$4" == '--ssl' ]; then
    sudo certbot certonly --agree-tos --email "${EMAIL}" -d "${DOMAIN}"
    sudo cp ./config/nginx_cert/"${DOMAIN}" /etc/nginx/sites-available/"${DOMAIN}"
fi