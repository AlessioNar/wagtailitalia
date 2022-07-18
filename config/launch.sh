#! /bin/bash

NAME=$1
USER=$2

if [ ! -d "/home/admin/logs" ]
then 
    mkdir /home/admin/logs
    touch /home/admin/gunicorn_supervisor.log
    touch /home/admin/nginx-error.log
    touch /home/admin/nginx-access.log
fi 

mkdir ../logs/${NAME}
touch ../logs/${NAME}/gunicorn_supervisor.log
echo "Created log files"

# Making supervisor aware of the new application
sudo supervisorctl reread 
echo "Supervisor list updated"

sudo supervisorctl add "${NAME}"
echo "added supervisor process group"

# Starting the application with supervisor
sudo supervisorctl start "${NAME}"

# Restart Nginx server
sudo systemctl restart nginx

exit 0

read -p "Please enter the email address to be https compliant and obtain a certificate from Let's Encrypt" EMAIL
sudo certbot certonly --agree-tos --email "${EMAIL}" -d "${DOMAIN}"
sudo cp ./config/nginx_cert/"${DOMAIN}" /etc/nginx/sites-available/"${DOMAIN}"

# Restarting the application with supervisor
sudo supervisorctl restart "${NAME}"
sudo systemctl restart nginx

# Copy media folder
#scp -r  "${SOURCE_DIR}"/"${NAME}"/"media" "${USER}"@"${IP_ADDRESS}":/home/"${USER}"/"${DOMAIN}"/media
 
