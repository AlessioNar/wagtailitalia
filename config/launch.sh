#! /bin/bash

NAME=$1
USER=$2

if [ ! -d "/home/admin/logs" ]
then 
    mkdir /home/admin/logs
    touch /home/admin/logs/gunicorn_supervisor.log
    touch /home/admin/logs/nginx-error.log
    touch /home/admin/logs/nginx-access.log
    echo "Generate system-wide log folders and files"
fi 


mkdir ../logs/${NAME}
touch ../logs/${NAME}/gunicorn_supervisor.log
echo "Created application log files"

# Configure Systemd files 
sudo systemctl daemon-reload
sudo systemctl enable --now gunicorn.socket
sudo systemctl restart gunicorn.socket
echo "Configured Systemd files"

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
 
