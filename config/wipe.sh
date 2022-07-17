NAME=$1
DOMAIN=$2
PASSWORD= source .secret


rm -rf "../${DOMAIN}"
$echo $PASSWORD | sudo -u postgres psql -c 'DROP DATABASE ${NAME};'

