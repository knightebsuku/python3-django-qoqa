import configparser
import random
import string
import os

from . import virtualenv
from . import database as db
from . import build

INIT_PROJECT_CONFIG = {}


def generate_key():
    """
    Generate Secret key for django
    """
    key = ''.join([random.SystemRandom().choice(string.ascii_letters +
                                                string.digits +
                                                string.punctuation)
                   for _ in range(50)])
    return key


def create_config(project_name: str):
    """
    Create configuration file for django project
    """
    print("[new] Creating configuration file")
    config = configparser.RawConfigParser()
    config['STATUS'] = {
        'Production': False
    }
    config['SECRET_KEY'] = {
        'value': ''.join(generate_key())
    }
    dev = INIT_PROJECT_CONFIG['DEV_DB']
    prod = INIT_PROJECT_CONFIG['PROD_DB']
    config['DEVELOPMENT_DATABASE'] = {k: v for k, v in dev.items()}
    config['PRODUCTION_DATABASE'] = {k: v for k, v in prod.items()}
    config['ALLOWED_HOSTS'] = {'Host': '127.0.0.1,locahost'}
    with open(project_name+'.cfg', 'w') as project_file:
        config.write(project_file)
    print('[new] Configuration file has been created')


def new(project_name: str):
    """
    Launch interactive console and setup new project
    """
    print("[new] Configuring New Django Project")
    db.setup()
    os.mkdir(project_name)
    os.chdir(project_name)
    virtualenv.create(project_name)
    create_config(project_name)
    print("[new] Project {} has been setup".format(project_name))


def build_project():
    """
    Build current django project.
    """
    print("[build] Checking that all requirements are met.")
    if os.path.isfile('setup.py'):
        print("[build] setup.py file exists")
    else:
        print("[build] setup.py file does not exist, creating.......")
        build.python_setup_file()

    if os.path.isfile('MANIFEST.in'):
        print('[build] MANIFEST.in file exists')
    else:
        print("[build] MANIFEST.in has not been created, creating......")
        build.manifest()

    if os.path.isfile('requirements.txt'):
        print("[build] requirements.txt file exists")
    else:
        print("[build] requirements.txt has not been created")
        build.requirements()

    if os.path.isdir('debian'):
        print("[build] debian directory exists")
    else:
        print("[build] debian directory does not exists, creating one....")
        build.debian()

    print('[build] building django project')
    build.dpkg()
