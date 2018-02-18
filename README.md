# Django-Rest-Framework-Mongoengine

A simple implementation of a Django Rest Framework backed by Mongoengine. It was built on top of this 
(https://github.com/BurkovBA/django-rest-framework-mongoengine-example) example with some added and changed features.

It has been tested on Ubuntu 16.04 and Windows 10.

## How does it work

This setup will allow you to host webpages and browseable RESTful APIs on top of the Django framework while making use of MongoDB as the main database.

The default Django admin structure is not implemented here. This service makes use of user-assigned token authentication, where a unique 
token is assigned to each user. This token is key for accessing features based on user privileges.

## Installation

A working instance of MongoDB is required. You'll also need the packages from requirements.txt, which can be easily installed with pip:
```
pip install -r requirements.txt
```
Obs.: as some of these packages may conflict with those currently installed in your machine, a good practice would be to perform a clean 
installation on a virtual environment.

Now, go to the server folder and run the server with
```
python manage.py runserver
```
You should be able to visit the Django Rest Framework index at http://localhost:8000/.

## A quick tour

As is, only superusers are allowed to create/modify/delete other users, but this can be changed at will. The user database is 
currently empty, so we have to manually create a superuser in order to make use of the framework.

Press ctrl + C to stop the server. Run the Django shell:
```
python manage.py shell
```
Create a superuser and assign to him a token:
```
from users.models import *
User.create_user(id='507f191e810c19729de860ea', # The unique identifier. Must be a valid ObjectId string.
                 name='Example Admin', 
	         username='example@admin.com', # Must be an email address. 
	         password='1234', 
                 is_active=True, 
                 is_staff=True, 
                 is_superuser=True)
tk, created = Token.objects.get_or_create(user='507f191e810c19729de860ea', username='user@test.com')
```
You should be able to find the 'user' and 'token' collections in MongoDB, each with one entry, under the 'django_test' database. 

Quit the Django shell and run the server again.

The users app comes with three simple functionalities:

1) Go to url http://localhost:8000/api/register. This allows for the creation of new users when superuser credentials are provided.

    Try creating a new user. Just make sure the id field gets an unique and valid ObjectId string and 'is active?' is set to True.

    Obs.: using ObjectIds as primary keys can be very useful in automated processes, 
and it's an easy way to guarantee the uniqueness of your data, but it also offers some drawbacks, specially in manual processes 
(like this one). This can be easily adjusted to your needs, though. For instance, one could use the username as the id. 

2) Go to url http://localhost:8000/api/auth. This will authenticate users and return their token keys. 

    Obtain your new user token key.

3) Go to http://localhost:8000/api/users/?token={your_new_user_token}. This is a RESTful API that exhibits all users recorded in 
your MongoDB. You should be able to see both users on this list.
