# Python3-qoqa 0.3.0

qoqa is a command line application to help setup django projects and package them as debian(.deb) packages._

* Qoqa is a Zulu word which roughly translates to collect.

_This project is mainly targeting small to medium sized django projects.__


#### Project dependencies
* devsctipts, 
* dpkg
* dpkg-dev 
* dh-virtualenv (>= 1.0)
* python3.5
* python3-venv
* python3-setuptools
* dh-python



We'll go through the usage of qoqa by creating a full django project, packaging and deploying it

## Creating a new Project
To create a new Django project the following command is used
```
$qoqa --new fruit
```
The above command will launch an interactive session asking a few questions.

_At this current stage only sqlite3 and postgresql databases are supported_

After the interactive session, qoqa will begin to download some packages from pip mainly

* Django
* Whitenoise
* Gunicorn
* Django-debug-toolbar

A directory with the following file structure will be created.

* fruit
    * env
    * fruit

The env directory houses all the virtual environment files.

* env
    * bin
    * lib
    * etc......

The fruit subdirectory will contain the traditional django project structure with some additional files and modifications

* fruit
    * fruit
    * fruit.cfg
    * ___init___.py
    * manage.py
    * production.cfg

The fruit.cfg file will contain some variables that will be used by django's settings.py file
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
hosts = 127.0.0.1,localhost
```
The production.cfg file looks somewhat similar to the fruit.cfg file, just that production will be set to True and the secret key value will be different.

When the django project gets placed in a production environment, the production.cfg will will be renamed to fruit.cfg since that is what the fruit/settings.py file will be looking for.

The fruit/settings.py has been modified to accomodate the fruit.cfg file.

The Modifed fruit/settings.py is created via the [django startproject template argument](https://docs.djangoproject.com/en/1.11/ref/django-admin/#django-admin-startproject)


So lets create a couple of django applications via the manage.py file (Dont forget to activate your virtual environment)
```
./manage.py startapp apple
./manage.py startapp banana
```
So now we have the following directory structure
* fruit
    * apple
    * banana
    * fruit
    * fruit.cfg
    * manage.py
    * production.cfg
	* __init__.py

So now we can continue on developing our project the usual way.

## Building the Django Project
So now you are ready to build and release your django project.

First we'll need create a `requirements.txt` file

```
$pip freeze > requirements.txt
```
_This command needs to be run in the same directory as the projects env directory._

```
$qoqa --build 0.1.0
```
_This command needs to be run in the same directory as the env directory_

The above command will generate the required files needed to begin the release process.

If it's the first time running the command it will generate the following files and directories

* fruit
    * debian
    * MANIFEST.in
    * requirements.txt
    * setup.py

### Debian directory
The debian directory contains the following files
* changelog - contains documentation about all the changes made to the package.
* compat - sets he compatibility level of the build.
* control - contains details about the project eg: Descriptions, dependencies etc.
* fruit.service - This is a systemd unit file that will run the django project as a service.
* postinst - This file contains details about what should happen after a package has been installed
* rules


If you want to read more about the debian directory and what type of files can be placed in here, you can read [this guide](https://www.debian.org/doc/manuals/maint-guide/)


### Setup.py
This is how the file will look

```
from setuptools import setup, find_packages


setup(
    name='fruit',
    version='0.1.0',
    packages=find_packages(),
    package_data={
        
    },
    # This is the data specified in the MANIFEST.in
    include_package_data=True,
)
```

The ```find_packages()``` function searches for all python packages thats why the __init__.py is there under the fruit directory.

We are treating the entire django project as a python package, allowing for the apple and banana packages to fall under the fruit package.


The ```package_data``` keyword argument is used to install other data files related to the package, so we'll be placing *.djhtml, *.css, and *.js files from our django applications.


```
package_data = {
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



## Releasing the django project
We are now ready to create a .deb file

```
$qoqa --release 0.1.0
```
The debian/changelog file will open up allowing you to make any final changes.
In the background, the above runs 

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

The application should now be running on 0.0.0.0:8000

##### Just two Notes

* The application is served via [Gunicorn](http://gunicorn.org/) and not Django's development server
* [Whitenoise](http://whitenoise.evans.io/en/stable/) handles the static files
