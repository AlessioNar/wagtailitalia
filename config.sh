NAME=wagtailitalia
DOMAIN=wagtail-italia.it
EMAIL=alessio.nardin@gmail.com

# Clone repository and add it to permissions
git clone https://github.com/AlessioNar/"${NAME}"
git config --global --add safe.directory /home/admin/"${NAME}"

# Change the name of the repository
mv $NAME $DOMAIN

cd $DOMAIN
virtualenv $NAME-env

source $NAME-env/bin/activate && \
pip install -r requirements.txt

# Make gunicorn script file executable for admin user
chown admin /home/admin/"${DOMAIN}"/"${NAME}"-env/bin/gunicorn_start
chown admin /etc/supervisor/conf.d/"${NAME}".conf
chmod u+x /home/admin/"${DOMAIN}"/deploy.sh
chown admin -R /home/admin/"${DOMAIN}"/media

# Create symbolic links
ln -s /etc/nginx/sites-available/"${DOMAIN}" /etc/nginx/sites-enabled/

certbot certonly --agree-tos --email "${EMAIL}" -d "${DOMAIN}"
