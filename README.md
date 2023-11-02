### Overview

A currency exchange ReST API made in Django with the following endpoints:

- GET `/currency/` - a list of all currencies currently available
- GET `/currency/<fst_currency>/<snd_currency>/` - a detail view of a currency pair's latest exchange rate

The admin panel is available with basic model interactions

### Requirements

- docker
- python

### Running

1. create a `.env` file in the `currency_exchange` app directory with the following env vars:
    - `SECRET_KEY` - Django's secret key
    - `MYSQL_ROOT_PASSWORD` - mysql db's root password
    - `MYSQL_DATABASE` - name of the db, that the server will use to store currency related data
    - `RABBITMQ_DEFAULT_USER` - rabbitmq username
    - `RABBITMQ_DEFAULT_USER` - rabbitmq password, the above credentials will be used to connect to the broker and
      schedule tasks
2. create a python virtual environment, activate it and install packages specified in `requirements.txt`
3. run `docker compose up -d` in the project's root directory
4. run migrations
5. start celery with `celery -A currency_exchange worker -B`, every 60 secs new currency exchange data will be fetched
   asynchronously
6. start the server with `python manage.py runserver`, the api will be available at http://localhost:8000/currency/

### Admin panel

To access the admin panel, create a superuser with `python manage createsuperuser` and use that created user to log
in to the panel