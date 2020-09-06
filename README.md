# Django Qoqa 1.0

Django-qoqa is a command-line application to create Django's projects and to package them as Debian packages.

* Qoqa is a Zulu word which roughly translates to 'to collect'.

This project is mainly a [concept](https://standalone.co.za/blog/django_debian_package/) but can used to test the idea

This application is intended for simple traditional Django projects that don't require complex setups or deployments.


## How to install  django-qoqa
Since this project involves some debian tools and commands, the best way to use it is to install it as a debian package, that way it will install all necessary debian packaging tools.

### Prebuilt
You can get the ready made .deb package [here](https://github.com/ebsuku/python3-django-qoqa/releases), if you don't want to build it yourself.

### Source

if you want to build this package from source

* Clone this repo

* ```dpkg-buildpackage -us -uc```

* ```sudo dpkg -i python3-dajngo-qoqa_1.0.0_amd64.deb ```

Since this debian package is installed via dpkg and not via apt, dependencies will not be automatically installed, so the initial setup will fail, to install the remaining dependencies run this

* ``` sudo apt -f install ```


## Tutorial

First create a top level directory for you project, this directory will contain the django project ,the virtual environment and other files that will be needed to build a debian package later on.

```
django-qoqa new fruit
```

where `fruit` is the name of the django project


The above command will launch an interactive session asking a couple of questions


```
[qoqa] Configuring New Django Project
Available django versions
1 - 2.2 LTS
2 - 3.1
[qoqa] select django version number [1]: 
```

This allows you to select a django version, this wil show the currently supported django versions.

```
Available Databases
1 - sqlite3
2 - postgresql
Development Database [1]: 

Production Database[1]:
1 - sqlite3
2 - postgresql
```

The supported databases are SQLite3 and PostgreSQL. 

If you select PostgreSQL you'll be asked questions about the database such as database name, port, username etc.

The assumption is that you already know these details for this small project.

The production settings will be saved in a configuration file (production.cfg) with some production settings already there such as secret key and debug status.

Once you have entered the relevant details, the default packages will be installed:

* Django
* Whitenoise
* Gunicorn
* Django-debug-toolbar

## Project Layout
Once you have created the project the folder structure will look as follows

```
|-- fruit
	|-- env3
	|-- production.cfg
	|-- fruit
		|-- manage.py
		|-- fruit
			|-- settings.py
			|-- etc
		|-- fruit.cfg
```
The ```production.cfg``` contains the config settings for production.

The ```fruit.cfg``` is the configuration file that is used during development

This is an example as to how the fruit.cfg file will look

```
[STATUS]
PRODUCTION = False

[SECRET_KEY]
VALUE = "$2[Qt8a_|j+kqF-2kdbn8ii4qn)?n8\gSXr$jHA)E[ga2]`uX

[DEVELOPMENT_DATABASE]
DATABASE = sqlite3
NAME = development_db.sqlite3

[ALLOWED_HOSTS]
HOSTS = localhost
```

The production.cfg file looks somewhat similar to the fruit.cfg file, just that production will be set to True and the secret key value will be different.

The ```fruit/settings.py``` file has been modified to accommodate the fruit.cfg file.

The modified fruit/settings.py is created via the [django startproject template argument](https://docs.djangoproject.com/en/1.11/ref/django-admin/#cmdoption-startproject-template)

At this point django-qoqa has done its job in creating the project.
After this step django-qoqa is no longer involved with the django project until you need to package the project as a debian package.

So lets create a couple of django applications via the manage.py file (Don't forget to activate your virtual environment)

```
./manage.py startapp apple
./manage.py startapp banana
```


## Building the Django Project
So after some development, creating views, adding static files, now its time to build the project

First we'll need create a `requirements.txt` file

```
$pip freeze -l > requirements.txt
```
**This file needs to sit in the top level directory, same directory containing env3**

```
$django-qoqa prepare --version 0.1.0
```
**This command needs to be run in the top level directory, same directory containing env3**

The above command will generate the required files needed to begin the build process.

This is how the top level directory looks like after the build process

```
|-- fruit
	|-- env3
	|-- debian
	|-- production.cfg
	|-- MANIFEST.in
	|-- requirements.txt
	|-- setup.py
	|-- fruit
		|-- apple
		|-- banana
		|-- __init__.py
		|-- etc
```

### Debian directory
The debian directory contains the following files:

* changelog - contains documentation about all the changes made to the package.
* compat - sets he compatibility level of the build.
* control - contains details about the project eg: Descriptions, dependencies etc.
* fruit.service - This is a systemd unit file that will run the django project as a service.
* postinst - This file contains details about what should happen after a package has been installed.
* rules - This files contains the instructions as to how to build the package.
* postrm - This file contains the details to remove the project once done

If you want to read more about the debian directory and what type of files can be placed in here, you can read [this guide](https://www.debian.org/doc/manuals/maint-guide/)
packaging for debian is a bit involved so the basic configurations have been created to make things easier.


### Setup.py
This is how the default file will look

```
from setuptools import setup, find_packages

PACKAGE_DATA = {}

setup(
    name='fruit',
    version='0.1.0',
    packages=find_packages(),
    package_data=PACKAGE_DATA,
    # This is the data specified in the MANIFEST.in
    include_package_data=True,
)
```

The ```find_packages()``` function searches for all python packages that's why the ```__init__.py``` is there under the fruit directory.

We are treating the entire django project as a python package, allowing for the apple and banana apps to fall under the fruit package.


The ```PACKAGE_DATA``` dictionary is used to collect all the static files (*.css, *.js, *.djhtml) from the django apps.

So it will look like the following.


```
PACKAGE_DATA = {
	'fruit': [
		'apple/static/apple/css/*.css',
		'apple/static/apple/js/*.js'
		'apple/templates/apple/*.djhtml',
		'banana/templates/banana/*.djhtml',
		'banana/static/banana/css/*.css',
		'banana/static/banana/js/*.js'
		etc........
		
	]
}
```


More details about the setup.py file and configurations can be found [here](http://setuptools.readthedocs.io/en/latest/setuptools.html)

### Manifest.in
In the manifest file allows you to add any other data files to be included in your python package.
In this case it will contain a start_gunicorn script, this will be used by the projects systemd unit file to start and stop the project.


## Releasing the django project
So all the above files and directory (manifest,setup, debian) can be configured to suit your needs, the main idea behind this project is that you wont have to make any configuration changes or minimal ones.
We are now ready to create a .deb file

```
$django-qoqa build --version 1.0.0
```
The debian/changelog file will open up allowing you to make any final changes.
Underneath, build runs

```
dpkg-buildpackage -us -uc
```
The whole building process and .deb creation is created by [dh-virtualenv](https://github.com/spotify/dh-virtualenv)

From the dh-virtualenv github page
> dh-virtualenv is a tool that aims to combine Debian packaging with self-contained virtualenv based Python deployments.


## Installing the .deb package
Once the build process is complete a fruit_0.1.0.deb file will be created.

To install the package

```
$sudo dpkg -i fruit_0.1.0.deb
```

This will install the package in 
```
/opt/venvs/fruit/
```

To start the application
```
$systemctl start fruit
```
The production.cfg file needs to be renamed to the projects name so in this tutorial fruit.cfg


The application should now be running on 0.0.0.0:8000


Just to reiterate this is just a concept project. 
I wanted to see if it is possible to debianize a django project and what it would involve in making it work.
