#!/bin/bash

# Update system
apt update && apt -y upgrade

# Create user admin and add it to sudo
adduser admin
adduser admin sudo

logout

ssh-copy-id -i ~/.ssh/id_rsa admin@139.162.184.175

exit 0