#!/bin/sh
# web edukiontzia abiaraztean: migrazioak aplikatu eta Apache abiarazi
set -e
python manage.py migrate --noinput
exec apache2ctl -D FOREGROUND
