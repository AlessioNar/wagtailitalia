#!/bin/bash

NAME=$1
DOMAIN=$2

WI_OCCURRENCES="s/wagtailitalia*"/"${NAME}"/"g"
INTEXT_OCCURRENCES="s/wagtailitalia"/"${NAME}"/"g"
DOMAIN_OCCURRENCES="s/wagtail-italia.it"/"${DOMAIN}"/"g"

# Renaming project variables so that they match the new project name
find . -iname "wagtailitalia*" | rename $WI_OCCURRENCES && rename $WI_OCCURRENCES
find . -iname "wagtail-italia.it" | rename $DOMAIN_OCCURRENCES
grep -RiIl "wagtailitalia" | xargs sed -i $INTEXT_OCCURRENCES
grep -RiIl "wagtail-italia.it" | xargs sed -i $DOMAIN_OCCURRENCES

exit 0

#ssh "${USER}"@"${IP_ADDRESS}" cd $DOMAIN && \
#chmod u+x deploy.sh && \
#./deploy.sh $NAME $DOMAIN
