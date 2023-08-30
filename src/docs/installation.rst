Installation
============

This content about, How can you installing the project on your system
For installing, follow the guidance step by step and don't worry for installing, it's very easy.

Tip 1: for linux user, you should use (python3) alternative (python) at first of command

Tip 2: for use dashboard you use this url:

``` http://127.0.0.1:8000/dashboard/ ```


Tip 3: for use admin panel, at first you should create super user and use this url:

``` http://127.0.0.1:8000/admin```


Tip 4: You should pay attention to port(8000), Possibility you use another port and for this you should use your
port alternative this port


Tip 5: In project we should have (.env) file and next to the manage.py and input this code:

```DEBUG=true
SECRET_KEY=django-insecure-mq11ioa63y^6ypgm^nwl(hrhempg6huelntq)9p53ae)x6f%xz
DATABASE_URL=postgres://postgres:asdf1234@localhost:5432/cafemenu ```


Step 1

Clone the project from this link:
------------------------------
``` $ git clone https://github.com/Ramin-RX7/CafeMenu.git ```


Step 2

Navigate to the repo directory
-----------------------------
``` $ cd CafeMenu ```


Step 3

Install required packages (requirements.txt)
------------------------------------------
``` $ python -m pip install -r requirements.txt ```


Step 4

Navigate to the project directory
--------------------------------
``` $ cd ./src/ ```


Step 5

Make/Apply migrations
----------------------
``` $ python manage.py makemigrations
$ python manage.py migrate ```


Step 6

Create super user
-----------------
for use admin panel and dashboard you should create super user

``` $ python manage.py createsuperuser ```


Step 7

Run the server
--------------
```$ python manage.py runserver```
