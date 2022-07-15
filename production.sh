PROJECT_NAME=$1
DOMAIN=$2

read -p "Enter ip address: " IP_ADDRESS
read -p "Enter user: " USER

REPOSITORY="https://github.com/AlessioNar/wagtailitalia"
echo $REPOSITORY

ssh "${USER}"@"${IP_ADDRESS}" git clone $REPOSITORY $DOMAIN

ssh "${USER}"@"${IP_ADDRESS}" cd $DOMAIN && \
chmod u+x deploy.sh && \
./deploy.sh $PROJECT_NAME $DOMAIN
