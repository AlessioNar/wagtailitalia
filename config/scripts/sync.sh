NAME=$2

SOURCE='/home/prometeo/Desktop/Developer/developers-italia/wagtailitalia'

rsync -a "${SOURCE}"/'blog/models.py' ./"${NAME}"/"blog"
rsync -a "${SOURCE}"/'home/models.py' ./"${NAME}"/"home"
rsync -a "${SOURCE}"/'streams/blocks.py' ./"${NAME}"/"streams"
rsync -a "${SOURCE}"/'flex/models.py' ./"${NAME}"/"flex"
rsync -a "${SOURCE}"/'menus/models.py' ./"${NAME}"/"menus"
rsync -a "${SOURCE}"/'site_settings/models.py' ./"${NAME}"/"site_settings"


rsync -a "${SOURCE}"/'templates/streams' ./"${NAME}"/"${NAME}"'/templates'
rsync -a "${SOURCE}"/'templates/home' ./"${NAME}"/"${NAME}"'/templates'
rsync -a "${SOURCE}"/'templates/flex' ./"${NAME}"/"${NAME}"'/templates'
rsync -a "${SOURCE}"/'templates/blog' ./"${NAME}"/"${NAME}"'/templates'

source ${NAME}-env/bin/activate && \
python manage.py makemigrations && \
python manage.py migrate
