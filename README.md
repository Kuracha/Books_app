# Books_app

To run Books_app by command line:
1. `python3 -m venv /path/to/venv`
2. `cd /path/to/venv/bin/activate`
3. `pip install -r requirements.txt`
4.`py manage.py makemigrations`
5.`py manage.py migrate`
6. `py manage.py createsuperuser`
7. `in directory with settings.py in project create and configure .env`
8. `./manage.py runserver` 
9. Go to `127.0.0.1:8000/path/to/template/`

To run Books_app in Docker in development mode:
1. `run docker and go to project root directory`
2. `docker-compose build`
3. `docker-compose up`
4. Go to `127.0.0.1:8000/path/to/template/ 
or http://192.168.99.100:8000/path/to/template/ `

To run Books_app in Docker in production mode:
1. `in directory with settings.py in project create 
and configure .env and .env.db`
2. `run docker and go to project root directory`
3. `docker-compose -f docker-compose.prod.yml up -d --build`
4. `docker-compose -f docker-compose.prod.yml up`
5. Go to `127.0.0.1:1337/path/to/template/ 
or http://192.168.99.100:1337/path/to/template/ `

## CONFIGURATION OF .env AND .env.db

I'm using postgresql db created in ElephantSQL so DB_ environments can be different depending 
on used database and service

.env
```
DEBUG=0 #set 1 if you want to run Dockerized app in production mode
ALLOWED_HOSTS=here are allowed hosts
SECRET_KEY=setkeyishere
APIKEY=setapikeyishere
DB_ENGINE=django.db.backends.postgresql
DB_DATABASE=postgresql_prod
DB_NAME=setdbdatabasenamhere
DB_USER=setdbusernamehere
DB_PASSWORD=setdbpasswordhere
DB_HOST=manny.db.elephantsql.com
DB_PORT=5432
```
.env.db
```
POSTGRES_USER=setdbusernamehere #same as DB_USER
POSTGRES_PASSWORD=setdbpasswordhere #same as DB_PASSWORD
POSTGRES_DB=postgresql_prod
```