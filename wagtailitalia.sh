#!/bin/bash
DIR=/home/admin/ensa-network.eu

NAME=$2
DOMAIN=$3

programname=$0

function usage {
    echo "usage: $programname"
    echo "./wagtailitalia.sh new NAME DOMAIN"
    echo "./wagtailitalia.sh production NAME DOMAIN"
    exit 1
}

if [ $1 == 'new' ];  then

	git clone https://github.com/AlessioNar/wagtailitalia $NAME

  cd $NAME

  WI_OCCURRENCES="s/wagtailitalia*"/"${NAME}"/"g"
  RENAME_FILE="s/wagtailitalia"/"${NAME}"/"g"
  DOMAIN_OCCURRENCES="s/wagtail-italia.it"/"${DOMAIN}"/"g"

  find . -iname "wagtailitalia*" | rename $WI_OCCURRENCES
  find . -iname "wagtailitalia*" | rename $WI_OCCURRENCES
  find . -iname "wagtail-italia.it" | rename $DOMAIN_OCCURRENCES

	grep -RiIl 'wagtailitalia' | xargs sed -i $RENAME_FILE
	grep -RiIl 'wagtail-italia.it' | xargs sed -i $DOMAIN_OCCURRENCES

	virtualenv $NAME-env
	source $NAME-env/bin/activate && \
	pip install -r requirements.txt && \
	python manage.py makemigrations blog flex home streams menus site_settings websites && \
	python manage.py migrate  && \
	python manage.py createsuperuser

  chmod u+x ./config/settings.sh

	exit 0

	# Here I need to create	an user
elif [ $1 == 'production' ];  then
  exec ./config/settings.sh $NAME $DOMAIN
  exit 0
fi
