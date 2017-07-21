import configparser
import random
import string
import os

from . import virtualenv
from . import database as db

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


def create_config():
    """
    Create configuration file for django project
    """
    print("Creating configuration file")
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
    with open(INIT_PROJECT_CONFIG['PROJECT_NAME']+'.cfg', 'w') as project_file:
        config.write(project_file)
    print('Configuration file has been created')


def new(project_name: str):
    """
    Launch interactive console and setup new project
    """
    print("Configure New Django Project")
    db.setup()
    os.mkdir(project_name)
    os.chdir(project_name)
    virtualenv.create(project_name)
    create_config()
    print("Project {} has been setup".format(project_name))
