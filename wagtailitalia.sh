#!/bin/bash

USER=admin
DIR=/home/admin/ensa-network.eu

PROJECT_NAME=$2

programname=$0

function usage {
    echo "usage: $programname"
    echo "When called without an argument, $programname executes all the following operations except for help, in this order."
    echo "  --github					Fetch github repository"
    echo "  --update      		Update pip packages"
    echo "  --collect-static  Collect static files"
    echo "  --create-superuser Creates the admin user"
    echo "  --migrate   			Writes and perform migration in database"
    echo "  --restart-app			Restarts the gunicorn application"
    echo "  --restart-server	Restarts the Nginx server"
    echo "  --help						Shows this function"
    exit 1
}

if [ $1 == 'new' ]; then

	git clone https://github.com/AlessioNar/wagtailitalia $PROJECT_NAME
  RENAME_STRING="s/wagtailitalia*"/"${PROJECT_NAME}"/"g"
	# Here I need to rename the names of the files in a recursive manner
  find . -iname "wagtailitalia*" | rename $RENAME_STRING
  find . -iname "wagtailitalia*" | rename $RENAME_STRING

	virtualenv $PROJECT_NAME-env
	source $PROJECT_NAME-env/bin/activate && \
	pip install -r $PROJECT_NAME/requirements.txt && \
	python $PROJECT_NAME/manage.py makemigrations && \
	python $PROJECT_NAME/manage.py migrate

	exit 0

	# Here I need to create	an user
fi

if [ $1 == 'run' ]; then

	source $PROJECT_NAME-env/bin/activate && \
	python manage.py collectstatic --noinput && \
	python manage.py runserver
	exit 0
fi

if [ $1 == 'createsuperuser' ]; then

	source $PROJECT_NAME-env/bin/activate && \
	python manage.py createsuperuser

fi
