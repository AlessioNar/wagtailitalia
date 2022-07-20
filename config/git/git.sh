#!/bin/bash

ORIGIN_URL=$1
USER=$2
NAME=$3

git remote rm origin $ORIGIN_URL
git init .
git add . -A
git commit -m "Initial commit"
git remote add origin https://github.com/$USER/$NAME
git push -u origin master
