Configuration
=============

In this content we talk about changes in settings file in config app.

change number 1

.env
-----

We add this code because our project can read env file

```env = Env()```

```env.read_env(".env")```

change number 2

SECRET KEY
----------

We add this code for run our server

```SECRET_KEY = env("SECRET_KEY")```

change number 3

Add context handler
-------------------

We add this code to become dynamic our website and some variables in every template we use

line 81

```"core.utils.context_handler"```

change number 4

Env for Database
----------------

We add a pass for database and use Postgresql for our database

line 93

change number 5

Time Zone
---------

We use False for our time zone because time zone has some bugs

line 129

```USE_TZ = False```

change number 6

Static
-----

We add static url and static DIR for some pictures that we always use these

line 134 to 138

```STATIC_URL = 'static/'```

```STATICFILES_DIRS = [
BASE_DIR / "static",]```


change number 7

AUTH USER MODEL
---------------

We add this line for create user with our authentication

line 148

```AUTH_USER_MODEL = "users.User"```


change number 8

AUTHENTICATION BACKENDS
-----------------------

This code is for our backends for authentication

line 150 to 153


```AUTHENTICATION_BACKENDS = [
'users.auth.UserAuthBackend',
'django.contrib.auth.backends.ModelBackend',]```


