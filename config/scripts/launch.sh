#! /bin/bash

NAME=$1
DOMAIN=$2
USER=$3



if [ ! -d "/home/admin/logs" ]
then 
    mkdir /home/admin/logs
    touch /home/admin/logs/gunicorn_supervisor.log
    touch /home/admin/logs/nginx-error.log
    touch /home/admin/logs/nginx-access.log
    echo "Generate system-wide log folders and files"
fi 


mkdir /home/admin/logs/${NAME}
touch /home/admin/logs/${NAME}/gunicorn.err.log
touch /home/admin/logs/${NAME}/gunicorn.out.log

echo "Created application log files"

cp /home/admin/${DOMAIN}/config/gunicorn/gunicorn_start /home/"${USER}"/"${DOMAIN}"/"${NAME}"-env/bin/gunicorn_start

source /home/admin/${DOMAIN}/${NAME}-env/bin/activate && \
sudo chmod guo+x /home/admin/${DOMAIN}/${NAME}-env/bin/gunicorn_start && \
deactivate

# Configure supervisor
sudo supervisorctl reread && sudo supervisorctl update
sudo supervisorctl start ${NAME}

sudo systemctl restart nginx

read -p "Please enter the email address to be https compliant and obtain a certificate from Let's Encrypt " EMAIL
sudo certbot certonly --agree-tos --email "${EMAIL}" -d "${DOMAIN}"
sudo cp /home/admin/${DOMAIN}/config/nginx/nginx_cert/${DOMAIN} /etc/nginx/sites-available/"${DOMAIN}"

# Restarting the application with supervisor
sudo supervisorctl restart "${NAME}"
sudo systemctl restart nginx

# Copy media folder
#scp -r  "${SOURCE_DIR}"/"${NAME}"/"media" "${USER}"@"${IP_ADDRESS}":/home/"${USER}"/"${DOMAIN}"/media

exit 0



 
