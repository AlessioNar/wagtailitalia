#!/bin/bash
USER=$1
IP_ADDRESS=$2
NAME=$3
DOMAIN=$4

# Dump database 
ssh $USER@$IP_ADDRESS 'pg_dump -F t hopeheatwaveseu > /home/admin/hope-heatwaves.eu/hopeheatwaveseu.tar'
echo "Dump database done"
mkdir /home/prometeo/Desktop/Developer/ensa-network.eu/hopeheatwaveseu/backup

# Copy database dump to backup server
scp $USER@$IP_ADDRESS:/home/admin/$DOMAIN/hopeheatwaveseu.tar /home/prometeo/Desktop/Developer/ensa-network.eu/hopeheatwaveseu/backup
echo "Copy database dump to backup server done"

# Copy media files to backup server
scp -r $USER@$IP_ADDRESS:/home/admin/hope-heatwaves.eu/media /home/prometeo/Desktop/Developer/ensa-network.eu/hopeheatwaveseu/backup/media
echo "Copy media files to backup server done"

