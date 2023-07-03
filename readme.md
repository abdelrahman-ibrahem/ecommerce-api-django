# ecommerce api 


# Steps for Runing the Application
- Setup environment
    - using python -m venv env 
    - source env/Scripts/activate => from git bash
    - ./env/Scripts/activate => from cmd
    - source env/bin/activate => Linux bash

- install dependencies
    - pip install -r requirements.txt

- Create .env file inside the ecommerce folder with these data
    - SECRET_KEY = test
    - IP_ADDRESS=localhost
    - DEBUG=1
    - ENGINE=django.db.backends.postgresql_psycopg2
    - DB_NAME=new_assignment
    - DB_USER=postgres
    - DB_PASSWORD=admin
    - DB_HOST=localhost
    - DB_PORT=5432

- makemigrations and migrate the models
    - python manage.py makemigrations
    - python manage.py migrate

- Run server
    - python manage.py runserver