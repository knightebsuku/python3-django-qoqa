# Qoqa 0.9.0

[Project Details](https://ebsuku.github.io/projects/qoqa/)

qoqa is a command line application to help setup django projects and package them as debian(.deb) packages.

* Qoqa is a Zulu word which roughly translates to collect.


A full tutorial can be found [here]()


## Quickstart

* Creating a new Project
``` 
$ qoqa new <projectname> --django <version>
```

* Build Project
```
$ qoqa build <version>
```

* Releasing Project
```
$ qoqa release <version>
```

* Only create virtualenv for an existing project
```
$ qoqa env <env_name> --django <version>
```

Once you have created the .deb file, you can simply run
```
dpkg -i <projectname>.deb
```
This will install the django project in /opt/venvs/<projectname>

A gunicorn systemd service will be created for the project.


#### Project dependencies
* devscripts, 
* dpkg
* dpkg-dev 
* dh-virtualenv (>= 1.0)
* python3.5 (>= 3.5)
* python3-venv(>= 3.5)
* python3-setuptools
* dh-python
* python3-colorama
