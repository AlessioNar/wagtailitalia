#!/bin/bash 

# Install required libraries
sudo apt install -y nginx python3-virtualenv supervisor python3-pip python3-dev libpq-dev curl postgresql postgresql-contrib rename certbot python3-certbot-nginx 
echo "Installing required packages"

sudo locale-gen "it_IT.UTF-8"
echo "Locale set to it_IT.UTF-8"

# Create postgres database and configure user admin
sudo su - postgres psql -c 'CREATE USER $USER WITH ENCRYPTED PASSWORD $DB_PASSWORD;'
echo "Added user $USER to postgres"

# Create log files
mkdir /home/$USER/logs
touch /home/$USER/logs/nginx-access.log
touch /home/$USER/logs/gunicorn_supervisor.log
echo "General log folders and files created"

# Configure Firewall
sudo ufw allow 'Nginx Full'
sudo ufw allow 'OpenSSH'
sudo ufw allow 80
sudo ufw --force enable
echo "Firewall configured"

# Verify configuration
sudo nginx -t
sudo systemctl restart nginx

logout

exit 0