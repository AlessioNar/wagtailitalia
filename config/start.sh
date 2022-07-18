#!/bin/bash

# Update system
apt update && apt -y upgrade

# Create user admin and add it to sudo
adduser admin
adduser admin sudo

logout

exit 0