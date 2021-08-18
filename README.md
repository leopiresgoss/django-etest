# Welcome to ETEST
### ETEST is a Django web application for the CS50's final project 

## Goal
The main objective is a web application that you can create tests and share them with anyone

## Installation
1.	Make sure that virtualenv and pip are already installed
2.	Download the project 
3.	Open your terminal and go to the location where your project is located
4.	Create the virtual environment in your shell: **$ virtualenv .**
5.	Check if the virtualenv is created (lib and bin folders and pyven.cfg must appear there)
6.	**$ source bin/activate**
7.	**$ pip install -r requirements.txt**
8.	**$ cd src**
9. 	**$ python manage.py makemigrations**
10.	**$ python manage.py migrate**
11.	Create superuser in order to access the admin¹: **$ python manage.py createsuperuser**
12. Run server: **$ python manage.py runserver**
13. With the link in your terminal, access **ETEST** in your browser :)

¹A superuser is necessary to access ETEST's creation area for the first time, you can add more users at http://127.0.0.1:8000/admin 

## Documentations
Check the documentations for more informations:

**Virtualenv** https://pypi.org/project/virtualenv/

**Pip** https://pip.pypa.io/en/stable/

**Django** https://docs.djangoproject.com/en/3.2/

## Acknowledgments
I would like to offer my special thanks to David J. Malan, the staff and all the CS50 community, it was a honor to take part of this course.
I would also like to thank FreeCodeCamp and Pyplane for providing excelent contents. 

Please, if you have any feedback, don't hesitate to contact me. Thank you.


