FROM python:3.6

RUN apt-get update && \
        apt-get install -y \
        build-essential \
        git

RUN pip install APScheduler Django django-heroku gunicorn psycopg2 psycopg2-binary requests django-crontab
RUN pip install git+git://github.com/django-extensions/django-extensions.git


ADD . /

EXPOSE 8000

WORKDIR msgbot
ENTRYPOINT python manage.py crontab add && python manage.py crontab add && gunicorn -b 0.0.0.0:8000 msgbot.wsgi
