# Catalyst Count

Catalyst Count is a web application built with Django, DB Sqlite 3, and Bootstrap. The application allows users to signup and login, upload a large volume of CSV data (up to 1GB), visualize the progress of the upload, and filter the data using a form. Once the user submits the form, the application displays the count of records based on the applied filters once user go on user add the user displays
users delete users.

## Features

- User authentication via django-allauth 
- File upload with progress visualization
- Data filtering and record counting
- Adding users displays users delete the users
- Bootstrap 4/5 for responsive UI

## Requirements

- Python 3.11.7
- Django 5.0.6
- DB Sqlite3
- Bootstrap 4/5
- django-allauth
- django-environ

## To Use Postgre SQL

- you can go to settings.py and provide the host name port in database to setup with Postegre SQL by default using DB Sqlite 3

## test.py

test.py is the maintained file to run unit testcases command to run python manage test catalystcountapp

## Run the Command for Migrations for make tables in database

python manage.py makemigrations
python manage.py migrate

## How to Run the application

python manage.py runserver

## Points to Note

1. After running python manage.py runserver click on signup create your user then click on sign in you will redirected to login page  

2. You can use my login credentials to login the application email id jainjammy344@gmail.com password JammyJain