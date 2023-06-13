# ecommerce api 


# Steps for Runing the Application
- Setup environment
- - using python -m venv env 
- - source env/Scripts/activate => from git bash
- - ./env/Scripts/activate => from cmd
- - source env/bin/activate => Linux bash
- install dependencies
- - pip install -r requirements.txt
- Create PostgreSQL database 
- - name => new_assignment
- - user => postgres
- - password => admin
- makemigrations and migrate the models
- - python manage.py makemigrations
- - python manage.py migrate
- Run server
- - python manage.py runserver