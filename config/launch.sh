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
python ./manage.py makemigrations && \
python ./manage.py migrate && \
python ./manage.py load

# Prompt the user to create at least a super user 
echo "Create a super user"

# Making supervisor 9aware of the new application
sudo supervisorctl reread 
sudo supervisorctl add "${NAME}"
sudo supervisorctl update

# Starting the application with supervisor
sudo supervisorctl start "${NAME}"

# Restart Nginx server
sudo systemctl restart nginx

# Copy media folder
 #scp -r  "${SOURCE_DIR}"/"${NAME}"/"media" "${USER}"@"${IP_ADDRESS}":/home/"${USER}"/"${DOMAIN}"/media

# Setting up SSL connection
 if [ $4 == '--ssl']; then
    certbot certonly --agree-tos --email "${EMAIL}" -d "${DOMAIN}"
    cp ./config/nginx_cert/"${DOMAIN}" /etc/nginx/sites-available/"${DOMAIN}"
fi