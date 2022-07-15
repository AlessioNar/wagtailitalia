#!/bin/bash
DIR=/home/admin/ensa-network.eu

PROJECT_NAME=$2
DOMAIN=$3

programname=$0

function usage {
    echo "usage: $programname"
    echo "./wagtailitalia.sh new PROJECT_NAME DOMAIN"
    echo "./wagtailitalia.sh production PROJECT_NAME DOMAIN"
    exit 1
}

if [[ $1 == 'new' ]]; then

	git clone https://github.com/AlessioNar/wagtailitalia $PROJECT_NAME

  cd $PROJECT_NAME

  RENAME_STRING="s/wagtailitalia*"/"${PROJECT_NAME}"/"g"
  RENAME_FILE="s/wagtailitalia"/"${PROJECT_NAME}"/"g"
  RENAME_DOMAIN="s/wagtail-italia.it"/"${DOMAIN}"/"g"

  find . -iname "wagtailitalia*" | rename $RENAME_STRING
  find . -iname "wagtailitalia*" | rename $RENAME_STRING
  find . -iname "wagtail-italia.it" | rename $RENAME_DOMAIN

	grep -RiIl 'wagtailitalia' | xargs sed -i $RENAME_FILE
	grep -RiIl 'wagtail-italia.it' | xargs sed -i $RENAME_DOMAIN

	virtualenv $PROJECT_NAME-env
	source $PROJECT_NAME-env/bin/activate && \
	pip install -r requirements.txt && \
	python manage.py makemigrations blog flex home streams menus site_settings websites && \
	python manage.py migrate  && \
	python manage.py createsuperuser

  chmod u+x ./config/settings.sh

	exit 0

	# Here I need to create	an user
elif [[ $1 == 'production']]; then

  exec ./config/settings.sh $PROJECT_NAME $DOMAIN

  exit 0
fi
if [[ $1 == 'run' ]]; then

	source $PROJECT_NAME-env/bin/activate && \
	python manage.py collectstatic --noinput && \
	python manage.py runserver
	exit 0
fi
