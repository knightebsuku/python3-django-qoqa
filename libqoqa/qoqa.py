import configparser
import random
import string
import os
import re

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


def production_config(project_name: str):
    """
    Create production.cfg file
    """
    print("[qoqa] Creating production.cfg file")
    config = configparser.RawConfigParser()
    config['STATUS'] = {
        'Production': True
    }
    config['SECRET_KEY'] = {
        'value': ''.join(generate_key())
    }
    db_conf = INIT_PROJECT_CONFIG['PROD_DB']
    config['PRODUCTION_DATABASE'] = {k: v for k, v in db_conf.items()}
    config['ALLOWED_HOSTS'] = {'Hosts': '127.0.0.1,localhost'}
    with open('production.cfg', 'w') as production_file:
        config.write(production_file)
    print("[qoqa] Configuration file for production created")


def development_config(project_name: str):
    """
    Create configuration file for django project
    """
    print("[qoqa] Creating configuration file")
    config = configparser.RawConfigParser()
    config['STATUS'] = {
        'Production': False
    }
    config['SECRET_KEY'] = {
        'value': ''.join(generate_key())
    }
    dev = INIT_PROJECT_CONFIG['DEV_DB']
    config['DEVELOPMENT_DATABASE'] = {k: v for k, v in dev.items()}
    config['ALLOWED_HOSTS'] = {'Hosts': '127.0.0.1,localhost'}
    with open(project_name+'.cfg', 'w') as project_file:
        config.write(project_file)
    print('[qoqa] Configuration file has been created')


def create(project_name: str):
    """
    Launch interactive console and setup new project
    """
    if project_name in ['new', 'build', 'release']:
        print('[qoqa] invalid project name: {}'.format(project_name))
        exit()
    print("[qoqa] Configuring New Django Project")
    if os.path.isdir(project_name):
        print("[qoqa] project directory already exists")
        exit()
    db.setup()
    os.mkdir(project_name)
    os.chdir(project_name)
    virtualenv.create(project_name)
    development_config(project_name)
    production_config(project_name)
    print("[qoqa] Project {} has been setup".format(project_name))


def new_build(version: str):
    """
    Update project version and check that all required files are present
    """
    if not re.match('[\d.]+', version):
        print('[qoqa] incorrect version format')
        exit()

    config = configparser.ConfigParser()
    config['DJANGO_PROJECT_VERSION'] = {'Version': version}
    with open('qoqa.cfg', 'w') as cfg:
        config.write(cfg)
    print("[prepare] Checking that all requirements are met.")
    if os.path.isfile('setup.py'):
        print("[qoqa] setup.py file exists")
    else:
        print("[qoqa] setup.py file does not exist, creating.......")
        build.python_setup_file()

    if os.path.isfile('MANIFEST.in'):
        print('[qoqa] MANIFEST.in file exists')
    else:
        print("[qoqa] MANIFEST.in has not been created, creating......")
        build.manifest()

    if os.path.isfile('start_gunicorn'):
        print('[qoqa] start_gunicorn file exists')
    else:
        print('[qoqa] Creating new start_gunicorn script')
        build.gunicorn_file()

    if os.path.isfile('requirements.txt'):
        print("[qoqa] requirements.txt file exists")
    else:
        print("[qoqa] requirements.txt has not been created")
        build.requirements()

    if os.path.isdir('debian'):
        print("[qoqa] debian directory exists, updating version")
        build.update_changelog(version)
    else:
        print("[qoqa] debian directory does not exists, creating one....")
        build.debian(version)
    print("[qoqa] Project ready to be built")

    print("[qoqa] finding django apps and updating static files")
    build.django_app_data()


def release(version):
    """
    Create .deb package.
    """
    if not re.match('[\d.]+', version):
        print("[qoqa] Incorrect version format")
        exit()
    config = configparser.ConfigParser()
    config.read('qoqa.cfg')
    if version != config['DJANGO_PROJECT_VERSION']['Version']:
        print("[qoqa] Build version and project version to not match")
        exit()
    print('[qoqa] Creating .deb for django project')
    build.dpkg(version)
