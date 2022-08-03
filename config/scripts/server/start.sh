#!/bin/bash

# Update system
apt update && apt -y upgrade

# Create user admin and add it to sudo
adduser admin
adduser admin sudo

logout

ssh-copy-id -i ~/.ssh/id_rsa $USER@$IP_ADDRESS

exit 0