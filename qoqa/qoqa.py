import configparser
import random
import string
import os

from . import virtualenv
from . import database as db

INIT_PROJECT_CONFIG = {}


def project_name():
    name = input("Project Name: ")
    if name == '':
        print("Please enter a project name")
        project_name()
    else:
        INIT_PROJECT_CONFIG['PROJECT_NAME'] = name


def database():
    """
    Setup database settings
    """
    dev_db = input("Development Database[sqlite3]: ")
    if dev_db == '':
        dev_db = 'sqlite3'
        INIT_PROJECT_CONFIG['DEV_DB'] = {
            'Database': dev_db,
            'name': 'development_db.sqlite3'
        }
    elif dev_db == 'postgresql':
        db.development_postgresql()
    else:
        print("Unknown database, currently supported database are"
              "sqlite3 and postgresql")
        database()

    prod_db = input("Production Database[sqlite3]: ")
    if prod_db == '':
        prod_db = 'sqlite3'
        INIT_PROJECT_CONFIG['PROD_DB'] = {
            'Database': prod_db,
            'name': 'production_db.sqlite3'
        }
    elif prod_db == 'postgresql':
        db.production_postgresql()
    else:
        print("Unknown database, currently supported database are"
              "sqlite3 and postgresql")
        database()
    print("Database settings configured")


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


def project():
    """
    Launch interactive console
    """
    print("Configure New Django Project")
    project_name()
    database()
    os.mkdir(INIT_PROJECT_CONFIG['PROJECT_NAME'])
    os.chdir(INIT_PROJECT_CONFIG['PROJECT_NAME'])
    virtualenv.create_virtualenv(INIT_PROJECT_CONFIG['PROJECT_NAME'])
    create_config()
    print(INIT_PROJECT_CONFIG['PROJECT_NAME'] + "has been setup")
