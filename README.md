# PWP SPRING 2020
# JOURNEY DIARY
# Group information
* Student 1. Maëlla Gheraia - maella.gheraia@gmail.com
* Student 2. Rémi Viotty - remi.viotty@student.oulu.fi
* Student 3. Radoslaw Wojaczek - radexw1@gmail.com

__Remember to include all required documentation and HOWTOs, including how to create and populate the database, how to run and test the API, the url to the entrypoint and instructions on how to setup and run the client__


<h2> All dependencies (external libraries) and how to install them </h2>
Flask - pip install Flask </br>
Pytest - pip install pytest </br>
Pytest-cov - pip install pytest-cov </br>
flask_restful - pip install flask_restful </br>
flask_sqlalchemy - pip install flask_sqlalchemy </br>
  
<h2>How to setup the framework </h2>
  
<h2> Define database and version utilized </h2>
MySQL is an Oracle-backed open source relational database management system based on SQL.  For this project we have used the 8.0.19.0 version which is the most recent version. 
Instructions how to setup the database framework and external libraries you might have used, or a link where it is clearly explained.
We used a MySQL Workbench. The following website is explaining how to setup MySQL Workbench : https://mysql.tutorials24x7.com/blog/how-to-install-mysql-workbench-8-on-windows

<h2>Instructions on how to setup and populate the database </h2>
				
Import .sql file with sql script which contains data for each column for each table in a database.

<h2> Instruction on how to run the tests of your database </h2>

Type in command line this command: pytest in the folder where db_test.py is. db_test and app should be in the same folder. Test will run immediately.

<h2> How to setup (e.g. modifying any configuration files) and run Journey Diary's RESTful API. </h2>

You have to link the app to the database in which you ran the script .sql by modifying the configuration file **config.py**.
This file contains 4 constants USERNAME, PASSWORD, ADDRESS and DATABASE, modify them to fit with your database.

Use the command flask run in the terminal. 

<h2>The URL to access your API (usually nameofapplication/api/version/)</h2>

http://127.0.0.1:5000/api/ (the entry point is http://127.0.0.1:5000/api/users/)

<h2> Instruction on how to run the tests of the implementation </h2>

Type in command line this command: pytest --cov-report term-missing --cov=resource
 in the folder where db_resource.py is. Test will run immediately. The coverage is the coverage of resource.

<h2> Instruction on how to setup and run the client </h2>

Type in command line this command (in project's folder directory): flask run. With this command server side will run, which is needed for proper working of client side.
Then, in the same folder, to setup client type in command line: "npm install", to install all of dependendies.
After installing, type in command line "npm start" to start all the scripts responsible for h
 in the folder where db_resource.py is. Test will run immediately. The coverage is the coverage of resource.

