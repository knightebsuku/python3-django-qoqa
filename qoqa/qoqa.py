import configparser
import random
import string
import os
import re

from colorama import Fore

from . import virtualenv
from . import database
from . import build

INIT_PROJECT_CONFIG = {}

# add libpq-dev
def django_version():
    """
    Specify a django version
    """
    dict_version = {"1": "2.2.*", "2": "3.1.*"}
    print(Fore.GREEN + "Avaliable django versions")
    print(Fore.GREEN + "1 - 2.2 LTS")
    print(Fore.GREEN + "2 - 3.1")
    while True:
        version = input(Fore.GREEN + "[qoqa] select django version number [1]: ")
        if version == "":
            return dict_version["1"]
        elif version not in ["1", "2"]:
            print(Fore.RED + "Invalid selection, options are 1 or 2")
        else:
            return dict_version[version]


def generate_key():
    """
    Generate Secret key for django
    """
    key = "".join(
        [
            random.SystemRandom().choice(
                string.ascii_letters + string.digits + string.punctuation
            )
            for _ in range(100)
        ]
    )
    return key


def configuration_file(status, db_config, project_name=None):
    """
    Create a configuration file based on the status(production, development)
    """
    config = configparser.RawConfigParser()
    print(Fore.GREEN + f"[qoqa] Creating {status} configuration file")

    config["SECRET_KEY"] = {"VALUE": "".join(generate_key())}
    config["ALLOWED_HOSTS"] = {"HOSTS": "127.0.0.1,localhost"}
    config["DATABASE"] = db_config
    config["STORAGE"] = {"LOCATION": "local"}

    if status == "development":
        config["STATUS"] = {"PRODUCTION": False}
        file_name = project_name

    elif status == "production":
        config["STATUS"] = {"PRODUCTION": True}
        file_name = "production"
    else:
        print(Fore.RED + "Unknown development status")
        exit()
    with open(f"{file_name}.cfg", "w") as status_file:
        config.write(status_file)
    print(Fore.GREEN + f"[qoqa] {status} configuration file created")


def create(project_name, template):
    """
    Launch interactive console and setup new project
    """
    if project_name in ["new", "build", "release"]:
        print(Fore.RED + "[qoqa] invalid project name: {}".format(project_name))
        exit()
    if os.path.isdir(project_name):
        print(Fore.RED + "[qoqa] project directory already exists")
        exit()
    print(Fore.GREEN + "[qoqa] Configuring New Django Project")
    version = django_version()
    os.mkdir(project_name)
    os.chdir(project_name)
    prod_config = database.create("production")
    dev_config = database.create("development")
    configuration_file("production", prod_config)
    configuration_file("development", dev_config, project_name)

    virtualenv.create(project_name, version, template)

    print(Fore.GREEN + f"[qoqa] Project {project_name} has been setup")


def check_requirements():
    """
    Check all requirements are met before creating a debian package
    """
    pass


def new_build(version: str):
    """
    First check that all requirements have been met.
    Build.
    """
    project_directory = os.path.basename(os.getcwd())

    print(Fore.GREEN + "[qoqa] Checking that all requirements are met.")
    if os.path.isfile("setup.py"):
        print(Fore.GREEN + "[qoqa] setup.py file exists")
    else:
        print(Fore.GREEN + "[qoqa] setup.py file does not exist, creating......")
        build.python_setup_file()

    if os.path.isfile("MANIFEST.in"):
        print(Fore.GREEN + "[qoqa] MANIFEST.in file exists")
    else:
        print(Fore.GREEN + "[qoqa] MANIFEST.in has not been created.")
        build.manifest()

    if os.path.isfile(os.path.join(project_directory, "start_gunicorn")):
        print(Fore.GREEN + "[qoqa] start_gunicorn file exists")
    else:
        print(Fore.GREEN + "[qoqa] Creating new start_gunicorn script")
        build.gunicorn_file()

    if os.path.isfile(os.path.join(project_directory, "__init__.py")):
        print(Fore.GREEN + "[qoqa] project __init__.py file exists")
    else:
        build.init_file()
        print(Fore.GREEN + "[qoqa]  __init__.py file created")

    if os.path.isfile("requirements.txt"):
        print(Fore.GREEN + "[qoqa] requirements.txt file exists")
    else:
        print(Fore.GREEN + "[qoqa] requirements.txt has not been created")
        build.requirements()

    if os.path.isdir("debian"):
        print(Fore.GREEN + "[qoqa] debian directory exists, updating version")
        build.update_changelog(version)
    else:
        print(Fore.GREEN + "[qoqa] debian directory does not exist")
        build.debian(version)
    print(Fore.GREEN + "[qoqa] Project ready to be built")

    print(Fore.GREEN + "[qoqa] finding django apps and updating static files")

    if build.django_app_data():
        """Ready to create .deb package"""
        build.dpkg(version)


def env(env_name, dj_version):
    """
    Only create virtualenv within project
    """
    env = virtualenv.SingleVenv(dj_version, with_pip=True)
    env.create(env_name)
