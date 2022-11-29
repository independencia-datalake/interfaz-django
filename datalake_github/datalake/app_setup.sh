# ! /bin/sh
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py loaddata core/fixtures/core/CI.json
python manage.py loaddata core/fixtures/core/UV.json
python manage.py loaddata core/fixtures/core/persona_inicial.json
python manage.py loaddata core/fixtures/core/telefono_inicial.json
python manage.py loaddata core/fixtures/core/correo_inicial.json
python manage.py loaddata core/fixtures/core/direccion_inicial.json
python manage.py loaddata core/fixtures/core/info_salud_inicial.json
python manage.py loaddata seguridad/fixtures/seguridad/CD.json
python manage.py loaddata seguridad/fixtures/seguridad/D.json