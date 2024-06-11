cd marketing_op/
yes | poetry run python manage.py makemigrations
yes | poetry run python manage.py migrate
poetry run gunicorn --bind :8000 --workers 3 marketing_op.wsgi:application
