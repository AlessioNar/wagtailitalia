#! /bin/bash

NAME=$1
DOMAIN=$2
USER=$3
DB_PASSWORD=$4
IP_ADDRESS=$5

echo "Copied production manage.py" 

# Print access credentials to the environmental variable
echo DOMAIN=$DOMAIN >> .env
echo DB_NAME=$NAME >> .env
echo DB_USER=$USER >> .env
echo DB_PASSWORD=$DB_PASSWORD >> .env
echo IP_ADDRESS=$IP_ADDRESS >> .env


# Generate a random SECRET_KEY and append it as an environmental variable
secret_key=$(openssl rand -base64 100 | tr -d '\n')
echo SECRET_KEY=$secret_key >> .env

# Launch application initialization process
source ./"${NAME}"-env/bin/activate && \
pip install -r ./requirements.txt && \
python ./manage.py collectstatic --noinput && \
python ./manage.py makemigrations blog flex home streams menus site_settings websites && \
python ./manage.py migrate && \
python ./manage.py load && \
python ./manage.py createsuperuser && \
deactivate