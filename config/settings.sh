NAME=$1
DOMAIN=$2
USER=$3

## Supervisor configuration
cp ./config/"${NAME}".conf /etc/supervisor/conf.d/"${NAME}".conf

## Gunicorn configuration
cp ./config/gunicorn_start /home/"${USER}"/"${DOMAIN}"/"${NAME}"-env/bin/gunicorn_start

## Copy Nginx configuration
cp "${NAME}"/config/nginx_nocert/"${DOMAIN}" /etc/nginx/sites-available/"${DOMAIN}"

# Set up manage.py to use production settings
cp ./config/manage.py ./manage.py

## Set up environmental variables for production environment
#scp -r  "${SOURCE_DIR}"/"${NAME}"/".env" "${USER}"@"${IP_ADDRESS}":/home/"${USER}"/"${DOMAIN}"/.env

# Copy deployment command
#scp -r  "${SOURCE_DIR}"/"${NAME}"/"deploy.sh" "${USER}"@"${IP_ADDRESS}":/home/"${USER}"/"${DOMAIN}"/deploy.sh

# Copy media folder
#scp -r  "${SOURCE_DIR}"/"${NAME}"/"media" "${USER}"@"${IP_ADDRESS}":/home/"${USER}"/"${DOMAIN}"/media

# Provide option for setting up certbot
#if [ $7 == '--ssl']; then
#  ## Nginx configuration
#  scp -r  "${SOURCE_DIR}"/"${NAME}"/"config/nginx_cert"/"${DOMAIN}" "${USER}"@"${IP_ADDRESS}":/etc/nginx/sites-available/"${DOMAIN}"
#  exit 0
#fi
