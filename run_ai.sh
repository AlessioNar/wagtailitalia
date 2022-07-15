#!/bin/bash
PROJECT_NAME=$1
DOMAIN=$2
programname=$0

function usage {
    echo "usage: $programname"
    echo "./deploy.sh new PROJECT_NAME DOMAIN"
    exit 1
}

  RENAME_STRING="s/wagtailitalia*"/"${PROJECT_NAME}"/"g"
  RENAME_FILE="s/wagtailitalia"/"${PROJECT_NAME}"/"g"
  RENAME_DOMAIN="s/wagtail-italia.it"/"${DOMAIN}"/"g"

  find . -iname "*" | rename $RENAME_STRING
  find . -iname "*" | rename $RENAME_STRING
  find . -iname "*" | rename $RENAME_DOMAIN

	grep -RiIl '' | xargs sed -i $RENAME_FILE
	grep -RiIl '' | xargs sed -i $RENAME_DOMAIN

	virtualenv $PROJECT_NAME-env
	source $PROJECT_NAME-env/bin/activate && \
	pip install -r requirements.txt && \
	python manage.py makemigrations blog flex home streams menus site_settings websites && \
	python manage.py migrate

	exit 0
