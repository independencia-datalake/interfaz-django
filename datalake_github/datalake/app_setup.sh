#! /bin/sh
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py loaddata core/fixtures/core/CI.json
python manage.py loaddata core/fixtures/core/UV.json
python manage.py loaddata core/fixtures/core/P0.json
python manage.py loaddata core/fixtures/core/T0.json
python manage.py loaddata core/fixtures/core/C0.json
python manage.py loaddata core/fixtures/core/D0.json
python manage.py loaddata seguridad/fixtures/seguridad/CD.json
python manage.py loaddata seguridad/fixtures/seguridad/D.json