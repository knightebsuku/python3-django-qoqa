# Qoqa 0.9.0

qoqa is a commandline application to create django projects and to package them as Debian(.deb) package files.

* Qoqa is a Zulu word which roughly translates to collect.

[Project Details](https://ebsuku.github.io/projects/qoqa/)

[Tutorial](https://ebsuku.github.io/tutorials/qoqa/qoqa/)

There are two ways to start using qoqa
* Download latest [release](https://github.com/ebsuku/python3-qoqa/releases) untar the file then build from source

```
dpkg-buildpackage -us -uc
```
* Use the already built deb file in the releases folder

```
sudo dpkg -i python3-qoqa_0.9.0_amd64.deb 
```


## Creating a new Project
To create a new Django project the following command is used

```
$qoqa new fruit
```
The above command will launch an interactive session asking a couple of questions
```
[qoqa] Configuring New Django Project
Avaliable django versions
1 - 1.11 LTS
2 - 2.0
[qoqa] select django version number [1]: 
```
This allows you to select a django version, these are the current supported django versions.

```
Avaliable Databases
1 - sqlite3
2 - postgresql
Development Database [1]: 

Production Database[1]: 
```
The supported databases are sqlite3 and postgresql. 

If you select postgresql you'll be asked question about the database such as database name, port, username etc.

For all my applications I already know what the database details are going to be, so I can fill out these details.

The production settings will be saved in a configuration file (production.cfg) with some production settings already there such as secret key and debug status.

Once you have entered the relevent details, the default packages will be installed:

* Django
* Whitenoise
* Gunicorn
* Django-debug-toolbar

## Project Layout
Once you have created the project the folder structure will look as follows

```
|-- fruit
	|-- env3
	|-- fruit
		|-- manage.py
		|-- fruit
			|-- settings.py
			|-- etc
		|-- fruit.cfg
		|-- production.cfg
```
The ```production.cfg``` contains the config settings for production.

The ```fruit.cfg``` is the configuration file that is used during development

This is an example as to how the fruit.cfg file will look
```
[STATUS]
production = False

[SECRET_KEY]
value = "$2[Qt8a_|j+kqF-2kdbn8ii4qn)?n8\gSXr$jHA)E[ga2]`uX

[DEVELOPMENT_DATABASE]
name = development_db.sqlite3
database = sqlite3

[ALLOWED_HOSTS]
hosts = localhost
```
The production.cfg file looks somewhat similar to the fruit.cfg file, just that production will be set to True and the secret key value will be different.

The ```fruit/settings.py``` file has been modified to accomodate the fruit.cfg file.

The modifed fruit/settings.py is created via the [django startproject template argument](https://docs.djangoproject.com/en/1.11/ref/django-admin/#cmdoption-startproject-template)

At this point qoqa has done its job in creating the project.

So lets create a couple of django applications via the manage.py file (Dont forget to activate your virtual environment)
```
./manage.py startapp apple
./manage.py startapp banana
```


## Building the Django Project
So now you are ready to build and release your django project.

First we'll need create a `requirements.txt` file

```
$pip freeze -l > requirements.txt
```
**This file needs to sit in the top level directory, same directory containing env3**

```
$qoqa build 0.1.0
```
**This command needs to be run in the top level directory, same directory containing env3**

The above command will generate the required files needed to begin the release process.

This is how the top level directory looks like after the build process

```
|-- fruit
	|-- env3
	|-- debian
	|-- qoqa.cfg
	|-- MANIFEST.in
	|-- requirements.txt
	|-- setup.py
	|-- fruit
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

If you want to read more about the debian directory and what type of files can be placed in here, you can read [this guide](https://www.debian.org/doc/manuals/maint-guide/)


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

The ```find_packages()``` function searches for all python packages thats why the ```__init__.py``` is there under the fruit directory.

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
In the mainfest file allows you to add any other data files to be included in your python package.


## Releasing the django project
We are now ready to create a .deb file

```
$qoqa release 0.1.0
```
The debian/changelog file will open up allowing you to make any final changes.
Underneath, release runs

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
If you included the production.cfg file in the MANIFEST.in file, the services will startup since the service first checks if there is a config file.

The application should now be running on 0.0.0.0:8000

## Installing dh-virtualenv >= 1.0

http://dh-virtualenv.readthedocs.io/en/latest/tutorial.html#step-1-install-dh-virtualenv

## Project dependencies
* devscripts, 
* dpkg
* dpkg-dev 
* dh-virtualenv (>= 1.0)
* python3.5 (>= 3.5)
* python3-venv(>= 3.5)
* python3-setuptools
* dh-python
* python3-colorama
