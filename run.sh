#!/bin/bash
NAME=$1
DOMAIN=$2

programname=$0

function usage {
    echo "usage: $programname new NAME DOMAIN"
    echo "Instantiates a new wagtailitalia instance in a remote server of choice, managing the backend and setting it up for production"
    exit 1
}

  WI_OCCURRENCES="s/wagtailitalia*"/"${NAME}"/"g"
  INTEXT_OCCURRENCES="s/wagtailitalia"/"${NAME}"/"g"
  DOMAIN_OCCURRENCES="s/wagtail-italia.it"/"${DOMAIN}"/"g"

  find . -iname "wagtailitalia*" | rename $WI_OCCURRENCES | find . -iname "wagtailitalia*" | rename $WI_OCCURRENCES
  find . -iname "wagtail-italia.it" | rename $DOMAIN_OCCURRENCES

	grep -RiIl '' | xargs sed -i $INTEXT_OCCURRENCES
	grep -RiIl '' | xargs sed -i $DOMAIN_OCCURRENCES

	virtualenv $NAME-env
	source $NAME-env/bin/activate && \
	pip install -r requirements.txt && \
	python manage.py makemigrations blog flex home streams menus site_settings websites && \
	python manage.py migrate

	exit 0
