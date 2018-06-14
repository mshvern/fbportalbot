web: sh -c 'cd msgbot && gunicorn msgbot.wsgi --log-file -'
clock: sh -c 'cd msgbot && python3 ./manage.py shell_plus < clocked_db.py'
