# Django-oAuth #

Django (/ˈdʒæŋɡoʊ/ jang-goh) is a free and open source web application framework, written in Python. A web framework is a set of components that helps you to develop websites faster and easier.


### Prerequisites ###

1 MySQL

1 libmysqlclient-dev ( apt-get install libmysqlclient-dev)

1 pip and python setuptools


### How do I get set up? ###

**Virtual environment**

Before we install Django we will get you to install an extremely useful tool to help keep your coding environment tidy on your computer. It's possible to skip this step, but it's highly recommended. Starting with the best possible setup will save you a lot of trouble in the future!

```
cd django-app
sudo apt-get install python-virtualenv
virtualenv venv
```


Start your virtual environment by running:

```
. venv/bin/activate

```
**Installing Django and other packages
**
```
pip install --upgrade pip
pip install -r requirement.txt
```


Change database settings based on your need in `mysite/settings.py`

```

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'name of the database',
        'USER': 'username',
        'PASSWORD': 'password',
        'HOST': '127.0.0.1',
        'PORT': '3306',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'"
            }
    }
}


```

**Note:** Make sure to first create the desirable database in MySQL. To create DB

```
mysql -u root -p

CREATE DATABASE myproject CHARACTER SET UTF8;
```
**
These steps are optional if you want to create a specific user for myproject database.**

Next, we will create a database user which we will use to connect to and interact with the database. Set the password to something strong and secure:

```

CREATE USER myprojectuser@localhost IDENTIFIED BY 'password';
```

Now, all we need to do is give our database user access rights to the database we created:

```

GRANT ALL PRIVILEGES ON myproject.* TO myprojectuser@localhost;
```

Flush the changes so that they will be available during the current session:

```

FLUSH PRIVILEGES;
```

**To make necessary migrations run these commands:
**

```

python manage.py makemigrations users  
python manage.py migrate  
```

### Errors ###

If you are behind a proxy server, For pip
` export https_proxy="https://proxy61.iitd.ac.in:3128" `

EnvironmentError: mysql_config not found

`sudo apt-get install libmysqlclient-dev`



create a superuser `python manage.py createsuperuser`

run server at port 8080 `python manage.py runserver 0.0.0.0:8080`
