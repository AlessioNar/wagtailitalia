PROJECT_NAME=wagtailitalia
DOMAIN=wagtail-italia.it
EMAIL=alessio.nardin@gmail.com

# Clone repository and add it to permissions
git clone https://github.com/AlessioNar/"${PROJECT_NAME}"
git config --global --add safe.directory /home/admin/"${PROJECT_NAME}"

# Change the name of the repository
mv $PROJECT_NAME $DOMAIN

cd $DOMAIN
virtualenv $PROJECT_NAME-env

source $PROJECT_NAME-env/bin/activate && \
pip install -r requirements.txt

# Make gunicorn script file executable for admin user
chown admin /home/admin/"${DOMAIN}"/"${PROJECT_NAME}"-env/bin/gunicorn_start
chown admin /etc/supervisor/conf.d/"${PROJECT_NAME}".conf
chmod u+x /home/admin/"${DOMAIN}"/deploy.sh
chown admin -R /home/admin/"${DOMAIN}"/media

# Create symbolic links
ln -s /etc/nginx/sites-available/"${DOMAIN}" /etc/nginx/sites-enabled/

certbot certonly --agree-tos --email "${EMAIL}" -d "${DOMAIN}"
