#!/bin/bash

NAME=$1
USER=$2
DB_PASSWORD=$4

echo DB_NAME=$NAME >> .env
echo DB_USER=$USER >> .env
echo DB_PASSWORD=$DB_PASSWORD >> .env