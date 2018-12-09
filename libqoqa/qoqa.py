import configparser
import random
import string
import os
import re

from colorama import Fore

from . import virtualenv
from . import database as db
from . import build

INIT_PROJECT_CONFIG = {}


def django_version():
    """
    Specify a django version
    """
    dict_version = {
        "1": "1.11.*",
        "2": "2.0.*",
        "3": "2.1.*"
    }
    print(Fore.GREEN + 'Avaliable django versions')
    print(Fore.GREEN + "1 - 1.11 LTS")
    print(Fore.GREEN + "2 - 2.0")
    print(Fore.GREEN + "3 - 2.1") 
    version = input(Fore.GREEN + "[qoqa] select django version number [1]: ")
    if version == '':
        return dict_version['1']
    elif version not in ['1', '2']:
        print(Fore.RED + 'Invalid selection, options are 1,2 or 3')
        django_version()
    return dict_version[version]


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
    print(Fore.GREEN + "[qoqa] Creating production.cfg file")
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
    print(Fore.GREEN + "[qoqa] Configuration file for production created")


def development_config(project_name: str):
    """
    Create configuration file for django project
    """
    print(Fore.GREEN + "[qoqa] Creating configuration file")
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
    print(Fore.GREEN + '[qoqa] Configuration file has been created')


def create(project_name: str):
    """
    Launch interactive console and setup new project
    """
    if project_name in ['new', 'build', 'release']:
        print(Fore.RED + '[qoqa] invalid project name: {}'.format(project_name))
        exit()
    if os.path.isdir(project_name):
        print(Fore.RED + "[qoqa] project directory already exists")
        exit()
    print(Fore.BLUE + "[qoqa] Configuring New Django Project")
    version = django_version()
    prod_db = db.setup()
    os.mkdir(project_name)
    os.chdir(project_name)
    virtualenv.create(project_name, version, prod_db)
    development_config(project_name)
    production_config(project_name)
    print(Fore.GREEN + "[qoqa] Project {} has been setup".format(project_name))


def new_build(version: str):
    """
    Update project version and check that all required files are present
    """
    if not re.match('[\d.]+', version):
        print(Fore.RED + '[qoqa] incorrect version format')
        exit()

    project_directory = os.path.basename(os.getcwd())
    config = configparser.ConfigParser()
    config['DJANGO_PROJECT_VERSION'] = {'Version': version}
    with open('qoqa.cfg', 'w') as cfg:
        config.write(cfg)
    print(Fore.GREEN + "[qoqa] Checking that all requirements are met.")
    if os.path.isfile('setup.py'):
        print(Fore.GREEN + "[qoqa] setup.py file exists")
    else:
        print(Fore.GREEN + "[qoqa] setup.py file does not exist, creating.")
        build.python_setup_file()

    if os.path.isfile('MANIFEST.in'):
        print(Fore.GREEN + '[qoqa] MANIFEST.in file exists')
    else:
        print(Fore.GREEN + "[qoqa] MANIFEST.in has not been created.")
        build.manifest()

    if os.path.isfile(os.path.join(project_directory, 'start_gunicorn')):
        print(Fore.GREEN + '[qoqa] start_gunicorn file exists')
    else:
        print(Fore.GREEN + '[qoqa] Creating new start_gunicorn script')
        build.gunicorn_file()

    if os.path.isfile(os.path.join(project_directory, '__init__.py')):
        print(Fore.GREEN + '[qoqa] project __init__.py file exists')
    else:
        build.init_file()
        print(Fore.GREEN + '[qoqa]  __init__.py file created')

    if os.path.isfile('requirements.txt'):
        print(Fore.GREEN + "[qoqa] requirements.txt file exists")
    else:
        print(Fore.GREEN + "[qoqa] requirements.txt has not been created")
        build.requirements()

    if os.path.isdir('debian'):
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
    if not re.match('[\d.]+', version):
        print(Fore.RED + "[qoqa] Incorrect version format")
        exit()
    config = configparser.ConfigParser()
    config.read('qoqa.cfg')
    if version != config['DJANGO_PROJECT_VERSION']['Version']:
        print(Fore.RED + "[qoqa] Build version and release version to not match")
        exit()
    print(Fore.GREEN + '[qoqa] Creating .deb for django project')
    build.dpkg(version)


def env(env_name, dj_version):
    """
    Only create virtualenv within project
    """
    env = virtualenv.SingleVenv(dj_version, with_pip=True)
    env.create(env_name)
