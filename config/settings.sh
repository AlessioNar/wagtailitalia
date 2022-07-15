PROJECT_NAME=$1
DOMAIN=$2

read -p "Enter ip address: " IP_ADDRESS
read -p "Enter user: " USER

## Supervisor configuration
scp -r ./"config"/"${PROJECT_NAME}".conf root@"${IP_ADDRESS}":/etc/supervisor/conf.d/"${PROJECT_NAME}".conf

## Gunicorn configuration
#scp -r ./"${PROJECT_NAME}"/"config"/"gunicorn_start" "${USER}"@"${IP_ADDRESS}":/home/"${USER}"/"${PROJECT_NAME}"/"${PROJECT_NAME}"-env/"bin/gunicorn_start"

## Wagtail configuration
#scp -r  "${SOURCE_DIR}"/"${PROJECT_NAME}"/".env" "${USER}"@"${IP_ADDRESS}":/home/"${USER}"/"${DOMAIN}"/.env
#scp -r  "${SOURCE_DIR}"/"${PROJECT_NAME}"/"manage.py" "${USER}"@"${IP_ADDRESS}":/home/"${USER}"/"${DOMAIN}"/manage.py
#scp -r  "${SOURCE_DIR}"/"${PROJECT_NAME}"/"settings/dev.py""${USER}"@"${IP_ADDRESS}":/home/"${USER}"/"${DOMAIN}"/"${PROJECT_NAME}"/settings/dev.py
#scp -r  "${SOURCE_DIR}"/"${PROJECT_NAME}"/"deploy.sh" "${USER}"@"${IP_ADDRESS}":/home/"${USER}"/"${DOMAIN}"/deploy.sh
#scp -r  /home/prometeo/Desktop/Developer/ensa-network.eu/ensanetworkeu/db.sqlite3 admin@139.162.184.175:/home/admin/form.ensa-network.eu/db.sqlite3
#scp -r  "${SOURCE_DIR}"/"${PROJECT_NAME}"/"media" "${USER}"@"${IP_ADDRESS}":/home/"${USER}"/"${DOMAIN}"/media

## Nginx configuration
#scp -r  "${SOURCE_DIR}"/"${PROJECT_NAME}"/"config/nginx_nocert"/"${DOMAIN}" "${USER}"@"${IP_ADDRESS}":/etc/nginx/sites-available/"${DOMAIN}"

#if [ $7 == '--ssl']; then
#  ## Nginx configuration
#  scp -r  "${SOURCE_DIR}"/"${PROJECT_NAME}"/"config/nginx_cert"/"${DOMAIN}" "${USER}"@"${IP_ADDRESS}":/etc/nginx/sites-available/"${DOMAIN}"
#  exit 0
#fi
