#!/bin/bash

#source $NAME-env/bin/activate && \

python manage.py flush --noinput
rm db.sqlite3
rm -rf media/images/*
python manage.py migrate && \
echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'password')" | python manage.py shell && \
python manage.py load 




