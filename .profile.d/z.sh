python manage.py collectstatic --noinput
python manage.py syncdb
python manage.py migrate --delete-ghost-migrations
