cd marketing_op/
yes | poetry run python manage.py makemigrations
yes | poetry run python manage.py migrate
yes | poetry run python manage.py collectstatic --noinput
poetry run python manage.py runserver 0.0.0.0:8000