#!/bin/bash

# Dump database 
ssh admin@139.162.184.175 'pg_dump -F t hopeheatwaveseu > /home/admin/hope-heatwaves.eu/hopeheatwaveseu.tar'
echo "Dump database done"

# Copy database dump to backup server
scp admin@139.162.184.175:/home/admin/hope-heatwaves.eu/hopeheatwaveseu.tar /home/prometeo/Desktop/Developer/ensa-network.eu/hopeheatwaveseu/hopeheatwaveseu.tar
echo "Copy database dump to backup server done"

# Copy media files to backup server
scp -r admin@139.162.184.175:/home/admin/hope-heatwaves.eu/media /home/prometeo/Desktop/Developer/ensa-network.eu/hopeheatwaveseu
echo "Copy media files to backup server done"

