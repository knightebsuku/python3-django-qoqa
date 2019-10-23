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


def django_version():
    """
    Specify a django version
    """
    dict_version = {"1": "1.11.*", "2": "2.2.*"}
    print(Fore.GREEN + "Avaliable django versions")
    print(Fore.GREEN + "1 - 1.11 LTS")
    print(Fore.GREEN + "2 - 2.2 LTS")
    while True:
        version = input(Fore.GREEN + "[qoqa] select django version number [1]: ")
        if version == "":
            return dict_version["1"]
        elif version not in ["1", "2"]:
            print(Fore.RED + "Invalid selection, options are 1 or 2")
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
            for _ in range(50)
        ]
    )
    return key


def create_production_settings():
    """
    Ask user if they want to setup production configurations
    """
    options = {"yes": True, "no": False}
    while True:
        status = input(
            Fore.GREEN + "Do you wan to create production configuration files? [yes]: "
        )
        if status not in ["yes", "no"]:
            print(Fore.RED + "Invalid option, please type yes or no")
        else:
            return options[status]


def configuration_file(status, db_config):
    """
    Create a configuration file based on the status(production, development)
    """
    config = configparser.RawConfigParser()
    print(Fore.GREEN + f"[qoqa] Creating {status} configuration file")

    config["SECRET_KEY"] = {"value": "".join(generate_key())}
    config["ALLOWED_HOSTS"] = {"Hosts": "127.0.0.1,localhost"}
    config["DATABASE"] = db_config

    if status == "development":
        config["STATUS"] = {"Production": False}

    elif status == "production":
        config["STATUS"] = {"Production": True}
    else:
        print(Fore.RED + "Unknown development status")
        exit()
    with open(f"{status}.cfg", "w") as status_file:
        config.write(status_file)
    print(Fore.GREEN + f"[qoqa] {status} configuration file created")


def create(project_name):
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
    prod_status = create_production_settings()
    os.mkdir(project_name)
    os.chdir(project_name)
    db_config = database.create("development")
    configuration_file("development", db_config)
    if prod_status:
        db_config = database.create("production")
        configuration_file("production", db_config)

    # virtualenv.create(project_name, version, prod_status)

    print(Fore.GREEN + f"[qoqa] Project {project_name} has been setup")


def new_build(version: str):
    """
    Update project version and check that all required files are present
    """
    if not re.match("[\d.]+", version):
        print(Fore.RED + "[qoqa] incorrect version format")
        exit()

    project_directory = os.path.basename(os.getcwd())
    config = configparser.ConfigParser()
    config["DJANGO_PROJECT_VERSION"] = {"Version": version}
    with open("qoqa.cfg", "w") as cfg:
        config.write(cfg)
    print(Fore.GREEN + "[qoqa] Checking that all requirements are met.")
    if os.path.isfile("setup.py"):
        print(Fore.GREEN + "[qoqa] setup.py file exists")
    else:
        print(Fore.GREEN + "[qoqa] setup.py file does not exist, creating.")
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
    build.django_app_data()


def release(version):
    """
    Create .deb package.
    """
    if not re.match("[\d.]+", version):
        print(Fore.RED + "[qoqa] Incorrect version format")
        exit()
    config = configparser.ConfigParser()
    config.read("qoqa.cfg")
    if version != config["DJANGO_PROJECT_VERSION"]["Version"]:
        print(Fore.RED + "[qoqa] Build version and release version to not match")
        exit()
    print(Fore.GREEN + "[qoqa] Creating .deb for django project")
    build.dpkg(version)


def env(env_name, dj_version):
    """
    Only create virtualenv within project
    """
    env = virtualenv.SingleVenv(dj_version, with_pip=True)
    env.create(env_name)
